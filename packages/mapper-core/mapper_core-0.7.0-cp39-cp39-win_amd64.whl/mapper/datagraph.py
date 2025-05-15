# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""The DataGraph class, representing a graph whose nodes are sets of data points."""

from __future__ import annotations

from typing import List, Literal, Optional, Tuple

import numpy as np

from mapper.affinities import affinity_functions
from mapper.graph import CSRGraph, EdgeListGraph
from mapper.neighborgraph import KNNGraph
from mapper.nerve import partition_vec_to_cover
from mapper.protocols import (
    AbstractGraph,
    CSRNeighborGraphLike,
    MultiResolutionGraph,
    NeighborGraphLike,
    SourceDataLike,
)
from mapper.serialization import DictConstructibleMixin


class DataGraph(
    AbstractGraph, NeighborGraphLike, CSRNeighborGraphLike, DictConstructibleMixin
):
    """A graph where nodes correspond with sets of data points.

    The idea is that nearly all of the operations involved in producing an
    output graph can be viewed as taking a DataGraph as input and producing one
    or more DataGraphs as output. This way the different operations in the
    pipeline can easily be mixed and matched.

    Presently, the class is designed to be backwards compatible with other graph
    structures used previously, so that it can serve as a replacement for all of
    them simultaneously. This may change in the future.

    Attributes:
        csr_graph: A CSRGraph containing the underlying graph structure
        n_data_points: The number of data points in the dataset represented by the graph
        node_membership: An array of length n_data_points indicating the node to
            which each data point belongs
        node_sets: A list of arrays giving the indices of data points belonging
            to each node.
        source_dataset: An optional attribute linking to the source data. This
            is present for backwards compatibility.
    """

    _serialization_version = 1

    def __init__(
        self,
        csr_graph: CSRGraph,
        node_membership: np.ndarray,
        source_dataset: Optional[SourceDataLike] = None,
        node_sets: Optional[List[np.ndarray]] = None,
        raw_knn_graph: Optional[KNNGraph] = None,
    ):
        self.csr_graph = csr_graph
        self.node_membership = node_membership
        self.n_data_points = len(node_membership)
        if node_sets is None:
            self.node_sets = partition_vec_to_cover(node_membership)
        else:
            self.node_sets = node_sets
        self.source_dataset = source_dataset
        self._edge_list_graph: Optional[EdgeListGraph] = None
        self._raw_knn_graph = raw_knn_graph

    def with_mask(self, mask: np.ndarray) -> DataGraph:
        masked_csr_graph = self.csr_graph.with_mask(mask)
        return DataGraph(
            masked_csr_graph,
            self.node_membership,
            source_dataset=self.source_dataset,
            node_sets=self.node_sets,
        )

    def partition_datagraph(
        self,
        partition_vec: np.ndarray,
        weight_attr: Optional[str] = None,
        mask: Optional[np.ndarray] = None,
        output_weights: Literal["constant", "sum", "normalized"] = "normalized",
        weight_normalize_power: float = 1.0,
    ) -> DataGraph:
        """Construct a partition graph for this graph. Keeps track of node sets."""
        edge_list_graph = self.csr_graph.partition_graph(
            partition_vec,
            weight_attr,
            mask,
            output_weights=output_weights,
            weight_normalize_power=weight_normalize_power,
        )
        if not weight_attr:
            # in this case csr_graph.partition_graph() set the "weight" edge_attr
            weight_attr = "weight"

        # TODO: normalize weights by number of data points rather than number of nodes?
        edge_list_graph.sort_edges(attr=weight_attr, descending=True)

        csr_graph = CSRGraph.from_edge_list(
            edge_list_graph.edge_mtx,
            n_nodes=edge_list_graph.n_nodes,
            # no node attrs defined (although we could add a method to aggregate them)
            edge_attrs=edge_list_graph.edge_attrs,
        )
        datagraph = DataGraph(csr_graph, partition_vec[self.node_membership])
        datagraph._edge_list_graph = edge_list_graph
        datagraph.source_dataset = self.source_dataset
        return datagraph

    def induced_subgraph(self, subset: np.ndarray) -> DataGraph:
        """Construct an induced subgraph, keeping track of node sets.

        Note that data points not included in nodes of this graph will have an
        index of -1 in the node_membership array.
        """
        csr_subgraph = self.csr_graph.induced_subgraph(subset)
        node_membership = self.node_membership.copy()
        node_membership[~np.isin(node_membership, subset)] = -1
        return DataGraph(csr_subgraph, node_membership=node_membership)

    # for backwards compatibility with DisjointPartitionGraph
    @property
    def nodes(self) -> List[np.ndarray]:
        return self.node_sets

    def _make_edge_list_graph(self) -> EdgeListGraph:
        return self.csr_graph.as_edge_list_graph(
            sort_attr="weight" if "weight" in self.csr_graph.edge_attrs else None,
            descending=True,
        )

    @property
    def edge_list(self) -> List[Tuple[int, int]]:
        if self._edge_list_graph is None:
            self._edge_list_graph = self._make_edge_list_graph()
        return [tuple(e) for e in self._edge_list_graph.edge_mtx]

    @property
    def edge_mtx(self) -> np.ndarray:
        if self._edge_list_graph is None:
            self._edge_list_graph = self._make_edge_list_graph()
        return self._edge_list_graph.edge_mtx

    @property
    def edge_weights(self) -> np.ndarray:
        if self._edge_list_graph is None:
            self._edge_list_graph = self._make_edge_list_graph()
        return self._edge_list_graph.edge_attrs["weight"]

    @property
    def n_edges(self) -> int:
        return len(self.edge_list)

    @property
    def edges(self):
        return [
            {"source": i, "target": j, "weight": w}
            for ((i, j), w) in zip(self.edge_list, self.edge_weights)
        ]

    # for compatibility with NeighborGraph
    @property
    def graph(self) -> DataGraph:
        return self

    @property
    def raw_graph(self) -> KNNGraph:
        """The underlying k-nearest-neighbor graph.

        May not be set if this is a partition graph.
        """
        if self._raw_knn_graph is None:
            raise AttributeError()
        return self._raw_knn_graph

    @raw_graph.setter
    def raw_graph(self, raw_graph):
        self._raw_knn_graph = raw_graph

    @property
    def data_matrix(self) -> Optional[SourceDataLike]:
        return self.source_dataset

    # for compatibility with CSRNeighborGraph
    @property
    def _neighbors(self) -> np.ndarray:
        return self.csr_graph._neighbors

    @property
    def _neighborhood_boundaries(self) -> np.ndarray:
        return self.csr_graph._neighborhood_boundaries

    @property
    def _distances(self) -> np.ndarray:
        """Underlying distances between data points.

        Raises a KeyError if this is not a symmetrized knn graph.
        """
        return self.csr_graph.edge_attrs["distance"]

    @_distances.setter
    def _distances(self, distances: np.ndarray):
        self.csr_graph.edge_attrs["distance"] = distances

    @property
    def _edge_ranks(self) -> np.ndarray:
        return self.csr_graph.edge_attrs["rank"]

    @_edge_ranks.setter
    def _edge_ranks(self, edge_ranks: np.ndarray):
        self.csr_graph.edge_attrs["rank"] = edge_ranks

    @property
    def N(self) -> int:
        return self.csr_graph.n_nodes

    def partition_modularity(
        self, partition_vec: np.ndarray, weight_attr: Optional[str] = None
    ):
        if weight_attr is None and "weight" in self.csr_graph.edge_attrs:
            weight_attr = "weight"
        return self.csr_graph.partition_modularity(partition_vec, weight_attr)

    def __data_dict__(self) -> dict:
        # TODO: source_dataset?
        return {
            "csr_graph": self.csr_graph,
            "node_membership": self.node_membership,
            "raw_knn_graph": self._raw_knn_graph,
        }

    def __eq__(self, other) -> bool:
        if not isinstance(other, DataGraph):
            return NotImplemented
        return (self is other) or all(
            (
                self.csr_graph == other.csr_graph,
                np.array_equal(self.node_membership, other.node_membership),
            )
        )


class HierarchicalDataGraph(MultiResolutionGraph, DictConstructibleMixin):
    _serialization_version = 1

    def __init__(
        self,
        levels: List[DataGraph],
        base_graph: DataGraph,
        neighbor_graph: Optional[NeighborGraphLike] = None,
        source_dataset: Optional[SourceDataLike] = None,
    ):
        self._levels = levels
        self.base_graph = base_graph
        self.source_dataset = source_dataset
        # do we ever need to set this independently?
        self.neighbor_graph: NeighborGraphLike = (
            neighbor_graph if neighbor_graph else base_graph
        )

    @property
    def levels(self):
        return self._levels

    @property
    def n_levels(self):
        return len(self._levels)

    def __data_dict__(self) -> dict:
        return {
            "levels": self._levels,
            "base_graph": self.base_graph,
            "neighbor_graph": (
                self.neighbor_graph
                if self.neighbor_graph is not self.base_graph
                else None
            ),
        }

    def __eq__(self, other) -> bool:
        if not isinstance(other, HierarchicalDataGraph):
            return NotImplemented
        return (
            self.base_graph == other.base_graph
            and self.n_levels == other.n_levels
            and all(l1 == l2 for l1, l2 in zip(self.levels, other.levels))
        )


def data_graph_from_csr_graph_with_distances_and_params(
    csr_graph: CSRGraph,
    node_membership: np.ndarray,
    affinity: str,
    distance_attr: str = "distance",
    params: Optional[dict] = None,
) -> DataGraph:

    edge_attrs = csr_graph.edge_attrs
    edge_attrs["weight"] = affinity_functions[affinity](edge_attrs[distance_attr])
    data_graph = DataGraph(csr_graph, node_membership=node_membership)
    if params is not None:
        for param, val in params.items():
            setattr(data_graph, param, val)
    return data_graph

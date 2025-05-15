# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
from __future__ import annotations

from typing import Dict, List, Literal, Optional, Tuple, Union

import networkx as nx
import numpy as np
import scipy.sparse

from mapper._csr_graph import (
    connected_components_masked_csr,
    get_edge_list_masked_csr,
    get_edge_list_masked_csr_with_attr_indices,
    partition_modularity,
    prune_filters_mask_csr,
)
from mapper.nerve import (
    partition_graph_edge_list_csr,
    partition_vec_to_cover,
    weighted_partition_graph_edge_list_csr,
)
from mapper.serialization import DictConstructibleMixin

# TODO: should we treat these as immutable? we can make the numpy arrays unwriteable

# immutability makes sense to me because I want to think of these either as
# final outputs of an algorithm, or as snapshots of an intermediate stage in the
# algorithm. The only algorithm we have that relies on a mutable graph is
# currently the hierarchical clustering.
# node merging or relinking algorithms might be more efficiently implemented
# with mutable graphs, though?
# immutability allows for a lot of zero-copy optimizations though

# I'm not sure if performance is the determinant here; rather, it's a question
# of how we want to interact with the graphs.

# one of the advantages? of immutability is lazy computation with caching. we
# can only compute the edge list, or edge ranks, or whatever, if you actually
# want it, and then automatically save it for later. does this matter?

# maybe we start by assuming it can be mutable, see if we actually want any
# mutability as we build algorithms, and if not, we can enforce immutability
# later.

# TODO: should there be parameters for things like rank pruning/masks?

# TODO: how important are masks? how inefficient is it to just copy to a subgraph?
# probably depends on the sparsity of the mask.
# masks might be the one exception to making edge attributes generic


def full_read_only(fill_val, shape: Tuple[int, ...], dtype=np.float32) -> np.ndarray:
    """Uses striding tricks for a memory-efficient np.full()."""
    return np.lib.stride_tricks.as_strided(
        np.array([fill_val], dtype=dtype),
        shape=shape,
        strides=(0,) * len(shape),
        # unfortunately, can't pass read-only buffers to Cython functions
        # writeable=False,
    )


def zeros_read_only(shape: Tuple[int, ...], dtype=np.float32) -> np.ndarray:
    return full_read_only(0, shape, dtype)


def get_block_boundaries(block_ids: np.ndarray, n_blocks: int) -> np.ndarray:
    """Produces an array of indices giving boundaries of constant regions in block_ids.

    Assumes block_ids is an array of integers in increasing order, and
    min(block_ids) >= 0, max(block_ids) < n_blocks.

    Output is an array of nondecreasing indices of length n_blocks + 1 such that
    for every i, block_ids[block_boundaries[i]:block_boundaries[i+1]] consists
    of all entries of block_ids equal to i.
    """
    block_boundaries = np.empty(n_blocks + 1, dtype=np.int32)

    block_boundaries[0 : block_ids[0] + 1] = 0
    block_diff = np.diff(block_ids, prepend=-1, append=n_blocks)
    change_points = np.flatnonzero(block_diff)
    change_point_sizes = block_diff[change_points]

    out_ix = 0
    for change_ix, change_size in zip(change_points, change_point_sizes):
        block_boundaries[out_ix : out_ix + change_size] = change_ix
        out_ix += change_size
    return block_boundaries


# TODO: can this be a cclass? would that even matter?
class CSRGraph(DictConstructibleMixin):
    """The CSRGraph is an arbitrary graph stored as a CSR matrix.

    It has nodes indexed from 0 to self.n_nodes - 1.

    Node and edge attributes can be stored in the node_attrs and edge_attrs
    properties. Each node attribute is stored in a Numpy array of length
    n_nodes, and each edge attribute in an array of length n_edges.

    Allows cheaply masking edges with the mask property, which behaves like a
    boolean-valued edge attribute. Edges with mask=False are ignored.

    This should be a reasonably efficient data structure that can represent most
    of the graphs we build and use. We can implement algorithms and
    serialization generically for this data structure, and encode graph types or
    roles in wrapper classes.
    """

    _serialization_version = 1

    def __init__(
        self,
        neighbors: np.ndarray,
        neighborhood_boundaries: np.ndarray,
        node_attrs: Optional[Dict[str, np.ndarray]] = None,
        edge_attrs: Optional[Dict[str, np.ndarray]] = None,
        mask: Optional[np.ndarray] = None,
    ):
        # TODO: should there be validation on construction?
        self._neighbors = neighbors
        self._neighborhood_boundaries = neighborhood_boundaries
        self.n_nodes = len(self._neighborhood_boundaries) - 1
        self.degrees = np.diff(self._neighborhood_boundaries)
        self.max_degree = np.max(self.degrees, initial=0)

        self.node_attrs = node_attrs if node_attrs is not None else {}
        self.edge_attrs = edge_attrs if edge_attrs is not None else {}
        self.mask = (
            mask
            if mask is not None
            else full_read_only(1, self._neighbors.shape, dtype=np.bool_)
        )

    @classmethod
    def from_edge_list(
        cls,
        edges: Union[List[Tuple[int, int]], np.ndarray],
        n_nodes: int,
        node_attrs: Optional[Dict[str, np.ndarray]] = None,
        edge_attrs: Optional[Dict[str, np.ndarray]] = None,
        add_reverse_edges: bool = True,
    ) -> CSRGraph:
        """Create a CSRGraph from an edge list and optional attributes.

        If add_reverse_edges=True, assume every edge is provided in exactly one
        direction.
        """
        if node_attrs is None:
            node_attrs = {}
        if edge_attrs is None:
            edge_attrs = {}

        for attr_name, arr in node_attrs.items():
            if len(arr) != n_nodes:
                raise ValueError(
                    f"node_attr '{attr_name}' has {len(arr)} values provided "
                    f"but n_nodes={n_nodes}."
                )
        for attr_name, arr in edge_attrs.items():
            if len(arr) != len(edges):
                raise ValueError(
                    f"edge_attr '{attr_name}' has {len(arr)} values provided "
                    f"but len(edges)={len(edges)}."
                )
        if len(edges) == 0:
            return CSRGraph(
                np.zeros(0, dtype=np.int32),
                np.zeros(n_nodes + 1, dtype=np.int32),
                node_attrs=node_attrs,
                edge_attrs=edge_attrs,
            )
        edge_mtx = np.array(edges)

        max_node_idx = np.max(edge_mtx)
        if max_node_idx >= n_nodes:
            raise ValueError(
                f"n_nodes={n_nodes} but there is a node with index {max_node_idx}."
            )

        if add_reverse_edges:
            reversed_edge_mtx = np.hstack(
                [edge_mtx[:, 1].reshape((-1, 1)), edge_mtx[:, 0].reshape((-1, 1))]
            )
            edge_mtx = np.vstack([edge_mtx, reversed_edge_mtx])
            edge_attrs = {
                key: np.concatenate([arr, arr]) for key, arr in edge_attrs.items()
            }
        edge_sort = np.argsort(edge_mtx[:, 0])
        sorted_edges = edge_mtx[edge_sort]

        # at this point, column 0 of sorted edges is a list of source nodes,
        # and column 1 is divided into blocks of neighbors for each source node
        # we just need to find the ranges of neighbors that belong to each source node
        neighborhood_boundaries = get_block_boundaries(sorted_edges[:, 0], n_nodes)
        neighbors = np.ascontiguousarray(sorted_edges[:, 1], dtype=np.int32)

        edge_attrs = {key: arr[edge_sort] for key, arr in edge_attrs.items()}

        return CSRGraph(
            neighbors,
            neighborhood_boundaries,
            node_attrs=node_attrs,
            edge_attrs=edge_attrs,
        )

    def _get_weights(self, affinity_attr: Optional[str]) -> np.ndarray:
        if affinity_attr is None:
            return full_read_only(1, self._neighbors.shape, dtype=np.float32)
        else:
            return self.edge_attrs[affinity_attr]

    # TODO: make this fast enough that it can be used in core algorithms
    def get_neighbors(self, node_ix: int) -> np.ndarray:
        return self._neighbors[
            self._neighborhood_boundaries[node_ix] : self._neighborhood_boundaries[
                node_ix + 1
            ]
        ]

    def get_edge_list(self) -> List[Tuple[np.int32, np.int32]]:
        return get_edge_list_masked_csr(
            self._neighbors,
            self._neighborhood_boundaries,
            zeros_read_only(self._neighbors.shape, dtype=np.int32),
            self.mask,
            1,
        )

    def as_edge_list_graph(
        self, sort_attr: Optional[str] = None, descending: bool = False
    ) -> EdgeListGraph:
        edge_list, attr_indices = get_edge_list_masked_csr_with_attr_indices(
            self._neighbors,
            self._neighborhood_boundaries,
            self.mask,
        )
        edge_mtx = np.array(edge_list, dtype=np.int32)
        edge_attrs = {k: arr[attr_indices] for k, arr in self.edge_attrs.items()}

        elg = EdgeListGraph(
            edge_mtx, self.n_nodes, node_attrs=self.node_attrs, edge_attrs=edge_attrs
        )
        if sort_attr:
            elg.sort_edges(sort_attr, descending)

        return elg

    def with_mask(self, mask: np.ndarray) -> CSRGraph:
        return CSRGraph(
            self._neighbors,
            self._neighborhood_boundaries,
            self.node_attrs,
            self.edge_attrs,
            mask,
        )

    def get_adjacency_matrix(
        self, weight_attr: Optional[str] = None
    ) -> scipy.sparse.csr_array:
        weights = self._get_weights(weight_attr)
        return scipy.sparse.csr_array(
            (weights, self._neighbors, self._neighborhood_boundaries),
            shape=(self.n_nodes, self.n_nodes),
        )

    def get_components(self) -> np.ndarray:
        return connected_components_masked_csr(
            self._neighbors,
            self._neighborhood_boundaries,
            zeros_read_only(self._neighbors.shape, dtype=np.int32),
            self.mask,
            1,
        )

    def refine_partitions(self, partitions: List[np.ndarray]) -> np.ndarray:
        """Connected components of each set in the joint partition refinement.

        Given a collection of partition vectors of the graph,
        computes the connected components of each set in their joint refinement.

        Works by masking all edges that go between partition sets in any of the
        partitions, and computing the connected components.
        """
        mask = prune_filters_mask_csr(
            self._neighbors,
            self._neighborhood_boundaries,
            partitions,
            np.zeros(len(partitions)),
        )
        return connected_components_masked_csr(
            self._neighbors,
            self._neighborhood_boundaries,
            zeros_read_only(self._neighbors.shape, dtype=np.int32),
            self.mask & mask,
            1,
        )

    # TODO: Cython
    def induced_subgraph(self, subset: np.ndarray) -> CSRGraph:
        """Returns the induced subgraph on the given set of vertices."""
        node_mask = np.zeros(len(self._neighborhood_boundaries) - 1, dtype=np.bool_)
        node_mask[subset] = 1
        # TODO: is it better to just push onto a list of edge indices?
        edge_mask = np.zeros(len(self._neighbors), dtype=np.bool_)
        # this is big enough, we will truncate later
        subset_neighbors = np.zeros_like(self._neighbors)
        subset_neighborhood_boundaries = np.zeros(len(subset) + 1, dtype=np.int32)

        out_idx = 0
        node_translation = {v: i for i, v in enumerate(subset)}
        for out_i, i in enumerate(subset):
            i_start = self._neighborhood_boundaries[i]
            i_end = self._neighborhood_boundaries[i + 1]
            for jdx in range(i_start, i_end):
                j = self._neighbors[jdx]
                if node_mask[j]:
                    edge_mask[jdx] = True
                    subset_neighbors[out_idx] = node_translation[j]
                    out_idx += 1
            subset_neighborhood_boundaries[out_i + 1] = out_idx

        subset_neighbors = subset_neighbors[:out_idx]
        subset_node_attrs = {
            attr: arr[node_mask] for attr, arr in self.node_attrs.items()
        }
        subset_edge_attrs = {
            attr: arr[edge_mask] for attr, arr in self.edge_attrs.items()
        }
        subset_edge_mask = self.mask[edge_mask]

        return CSRGraph(
            subset_neighbors,
            subset_neighborhood_boundaries,
            subset_node_attrs,
            subset_edge_attrs,
            subset_edge_mask,
        )

    def partition_graph(
        self,
        partition_vec: np.ndarray,
        weight_attr: Optional[str] = None,
        mask: Optional[np.ndarray] = None,
        output_weights: Literal["constant", "sum", "normalized"] = "normalized",
        weight_normalize_power: float = 1.0,
    ) -> EdgeListGraph:
        if mask is None:
            mask = self.mask

        cover = partition_vec_to_cover(partition_vec)

        if output_weights == "constant":
            edge_list = partition_graph_edge_list_csr(
                self._neighbors,
                self._neighborhood_boundaries,
                zeros_read_only(self._neighbors.shape, dtype=np.int32),
                mask,
                1,
                partition_vec,
                cover,
            )
            edge_mtx = np.array(edge_list, dtype=np.int32)
            weights = full_read_only(1, (edge_mtx.shape[0],), dtype=np.float32)

        else:
            weights = self._get_weights(weight_attr)
            edge_mtx, weights = weighted_partition_graph_edge_list_csr(
                self._neighbors,
                weights,
                self._neighborhood_boundaries,
                zeros_read_only(self._neighbors.shape, np.int32),
                mask,
                1,
                partition_vec,
                cover,
                normalize_weights=output_weights == "normalized",
                normalize_power=weight_normalize_power,
            )

        # TODO: should allow reducing over other edge and node attributes?
        # TODO: should this just return a CSRGraph?
        return EdgeListGraph(
            edge_mtx,
            len(cover),
            node_attrs={"data_points": cover},
            edge_attrs={(weight_attr if weight_attr else "weight"): weights},
        )

    def partition_modularity(
        self,
        partition_vec: np.ndarray,
        weight_attr: Optional[str] = None,
    ):
        """Compute the modularity score for the given partition on this graph.

        This is the difference between the (weighted) fraction of edges inside
        each set of the partition and the expected fraction of edges in that set if
        the graph were randomly rewired while preserving node degrees.
        """
        weights = self._get_weights(weight_attr)

        # TODO: update to more full-featured version
        return partition_modularity(
            self._neighbors, weights, self._neighborhood_boundaries, partition_vec
        )

    def as_networkx(self) -> nx.Graph:
        """Returns this graph as a networkx.Graph instance."""
        # TODO: edge attributes
        g = nx.Graph()
        node_list = (
            (i, {attr: arr[i] for attr, arr in self.node_attrs.items()})
            for i in range(self.n_nodes)
        )
        g.add_nodes_from(node_list)
        g.add_edges_from(self.get_edge_list())
        return g

    def __data_dict__(self) -> dict:
        # TODO(maybe): support for serializing complex node_attrs
        # (specifically, arrays of arrays)
        return {
            "neighbors": self._neighbors,
            "neighborhood_boundaries": self._neighborhood_boundaries,
            "node_attrs": self.node_attrs,
            "edge_attrs": self.edge_attrs,
            "mask": self.mask,
        }

    def __eq__(self, other) -> bool:
        if not isinstance(other, CSRGraph):
            return NotImplemented
        try:
            if self is other:
                # avoid doing expensive compraisons when they are all the same object
                return True
            return all(
                (
                    np.array_equal(self._neighbors, other._neighbors),
                    np.array_equal(
                        self._neighborhood_boundaries, other._neighborhood_boundaries
                    ),
                    np.all(self.mask == other.mask),  # handles None
                    all(
                        np.array_equal(self.node_attrs[a], other.node_attrs[a])
                        for a in set(self.node_attrs.keys()).union(other.node_attrs)
                    ),
                    all(
                        np.array_equal(self.edge_attrs[a], other.edge_attrs[a])
                        for a in set(self.edge_attrs.keys()).union(other.edge_attrs)
                    ),
                )
            )
        except KeyError:
            return False
        except ValueError:  # if arrays don't broadcast against each other
            return False


class EdgeListGraph(DictConstructibleMixin):
    _serialization_version = 1

    def __init__(
        self,
        edge_mtx: np.ndarray,
        n_nodes: int,
        node_attrs: Optional[Dict[str, List]] = None,
        edge_attrs: Optional[Dict[str, np.ndarray]] = None,
    ):
        self.edge_mtx = edge_mtx
        self.n_nodes = n_nodes

        self.node_attrs = node_attrs if node_attrs is not None else {}
        self.edge_attrs = edge_attrs if edge_attrs is not None else {}

    def sort_edges(self, attr: str, descending: bool = False):
        if self.edge_mtx.shape[0] == 0:
            return

        sort_idx = np.argsort(self.edge_attrs[attr])
        if descending:
            sort_idx = sort_idx[::-1]
        self.edge_mtx = self.edge_mtx[sort_idx, :]
        self.edge_attrs = {k: arr[sort_idx] for k, arr in self.edge_attrs.items()}

    def __data_dict__(self) -> dict:
        return {
            "edge_mtx": self.edge_mtx,
            "n_nodes": self.n_nodes,
            "node_attrs": self.node_attrs,
            "edge_attrs": self.edge_attrs,
        }

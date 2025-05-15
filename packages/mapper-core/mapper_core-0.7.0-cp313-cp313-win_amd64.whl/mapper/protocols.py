# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""Protocol classes defining interfaces."""

from abc import abstractmethod
from typing import (
    Collection,
    Dict,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    runtime_checkable,
)

import numpy as np


class KNNGraphLike(Protocol):
    _neighbors: np.ndarray
    _distances: np.ndarray

    @property
    def edge_list(self) -> List[Tuple[np.int32, np.int32]]: ...

    def as_networkx(self): ...


class CSRNeighborGraphLike(Protocol):
    _neighbors: np.ndarray
    _neighborhood_boundaries: np.ndarray
    _distances: np.ndarray


class NeighborGraphLike(Protocol):
    @property
    def raw_graph(self) -> KNNGraphLike: ...

    @property
    def graph(self) -> CSRNeighborGraphLike: ...


class SourceDataLike(Protocol):
    @property
    def X(self) -> np.ndarray: ...

    @property
    def shape(self) -> tuple: ...


@runtime_checkable
class AbstractGraph(Protocol):
    """A graph whose nodes represent disjoint subsets of a source dataset."""

    source_dataset: Optional[SourceDataLike]
    """An optional reference to the dataset used to create this graph."""

    node_membership: np.ndarray
    """An array with one entry for each data point indicating the node to
    which that data point belongs."""

    @property
    @abstractmethod
    def nodes(self) -> Sequence[Collection]:
        """A list with one entry for each node, where entry i contains the data
        point ids represented in node i."""

    @property
    @abstractmethod
    def edge_list(self) -> List[Tuple[int, int]]:
        """List of tuples ``(i,j)`` representing edges i->j.

        Edges should be interpreted as undirected, and only the direction with
        ``i < j`` will be included in the list.
        """

    @property
    @abstractmethod
    def edge_mtx(self) -> np.ndarray:
        """A list of edges in numpy array form.

        Array is of shape ``(n_edges, 2)``, and ``edge_mtx[k, :] = [i, j]`` for an edge
        i->j.
        """

    @property
    @abstractmethod
    def edge_weights(self) -> np.ndarray:
        """Nonnegative weights for each edge."""

    @property
    @abstractmethod
    def n_edges(self) -> int:
        """Number of edges in the graph."""

    @property
    @abstractmethod
    def edges(self) -> List[Dict]:
        """A list of dictionaries representing data for each edge.

        The dictionary for an edge will contain at least "source", "target", and
        "weight" keys, but may contain additional data.
        """

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(source_dataset={self.source_dataset}, "
            f"n_nodes={len(self.nodes)}, n_edges={self.n_edges})"
        )


@runtime_checkable
class MultiResolutionGraph(Protocol):
    """A graph with multiple resolution scales.

    There are n_levels different graphs arranged in a hierarchical way. Each
    node of the graph at level i represents a subset of data points, and is a
    subset of some node of the graph at each level j > i.
    """

    n_levels: int
    """The number of different coarseness levels in the graph"""

    source_dataset: Optional[SourceDataLike]
    """An optional reference to the dataset used to create this graph."""

    neighbor_graph: NeighborGraphLike
    """An underlying graph of nearest neighbors of points in the dataset."""

    @property
    @abstractmethod
    def levels(self) -> List[AbstractGraph]:
        """A list of graphs representing the dataset at multiple resolution scales."""

    def __len__(self):
        return self.n_levels

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(source_dataset={self.source_dataset}, "
            f"n_levels={self.n_levels})"
        )

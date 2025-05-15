# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""Graph pruning predicates."""
from abc import abstractmethod
from typing import Union

import numpy as np

from mapper._csr_graph import (
    prune_filter_mask_csr,
    prune_filter_mask_csr_frac,
    prune_filter_mask_csr_local,
)
from mapper.protocols import CSRNeighborGraphLike


# this is a class rather than just a standalone function so we can serialize it
# more easily.
class GraphPruningPredicate:
    @abstractmethod
    def prune_graph(self, graph: CSRNeighborGraphLike) -> np.ndarray:
        """Returns a mask for the edges of a CSRNeighborGraph."""


class TrivialPruningPredicate(GraphPruningPredicate):
    """Performs no pruning."""

    def prune_graph(self, graph: CSRNeighborGraphLike) -> np.ndarray:
        return np.ones(graph._neighbors.shape[0], dtype=np.bool_)


class FunctionValuePruningPredicate(GraphPruningPredicate):
    """Prunes the edges of a graph based on values of a function on its nodes.

    prune_vals should be a 1-d array with the same number of data points as the
    graph, and pruning_threshold is a nonnegative number. An edge between two
    nodes whose function values differ by more than pruning_threshold will be
    masked off.
    """

    def __init__(self, prune_vals: np.ndarray, pruning_threshold: Union[int, float]):
        self.prune_vals = prune_vals
        self.pruning_threshold = pruning_threshold

    def prune_graph(self, graph: CSRNeighborGraphLike) -> np.ndarray:
        # pylint: disable=protected-access
        mask = prune_filter_mask_csr(
            graph._neighbors,
            graph._neighborhood_boundaries,
            self.prune_vals,
            self.pruning_threshold,
        )
        return mask


class PercentOverlapPruningPredicate(GraphPruningPredicate):
    def __init__(
        self,
        filter_vals: np.ndarray,
        range_partition: np.ndarray,
        domain_partition: np.ndarray,
        pruning_threshold: float,
    ):
        self.filter_vals = filter_vals
        self.range_partition = range_partition
        self.domain_partition = domain_partition
        self.pruning_threshold = pruning_threshold
        interval_widths = np.diff(self.range_partition)
        self.upper_bounds = np.zeros_like(interval_widths)
        self.upper_bounds[:-1] = range_partition[1:-1] + (
            pruning_threshold * interval_widths[1:]
        )
        self.upper_bounds[-1] = np.inf
        self.lower_bounds = np.zeros_like(interval_widths)
        self.lower_bounds[1:] = range_partition[1:-1] - (
            pruning_threshold * interval_widths[:-1]
        )
        self.lower_bounds[0] = -np.inf

    def prune_graph(self, graph: CSRNeighborGraphLike) -> np.ndarray:
        mask = prune_filter_mask_csr_frac(
            graph._neighbors,
            graph._neighborhood_boundaries,
            self.filter_vals,
            self.domain_partition,
            self.lower_bounds,
            self.upper_bounds,
        )
        return mask


class LocalFunctionValuePruningPredicate(GraphPruningPredicate):
    """Prunes edges based on a function value only within a subset of nodes."""

    def __init__(
        self,
        prune_vals: np.ndarray,
        pruning_threshold: Union[int, float],
        domain: np.ndarray,
    ):
        self.prune_vals = prune_vals
        self.pruning_threshold = pruning_threshold
        self.domain = domain

    def prune_graph(self, graph: CSRNeighborGraphLike) -> np.ndarray:
        # pylint: disable=protected-access
        mask = prune_filter_mask_csr_local(
            graph._neighbors,
            graph._neighborhood_boundaries,
            self.prune_vals,
            self.pruning_threshold,
            self.domain,
        )
        return mask

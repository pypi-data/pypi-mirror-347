# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# ruff: noqa: E402
"""Implementation of xshop-Mapper."""
import os

os.environ["KMP_WARNINGS"] = "FALSE"

from mapper.data_partition import (
    DataPartition,
    Filter,
    FilterFunction,
    LocalFilter,
    TrivialFilter,
)
from mapper.datagraph import DataGraph, HierarchicalDataGraph
from mapper.filter_function import (
    DensityFunction,
    EccentricityFunction,
    FilterSource,
    RawFunction,
)
from mapper.graph import CSRGraph, EdgeListGraph
from mapper.hierarchical_partition import (
    AverageLinkageClustering,
    FlattenedHierarchicalPartition,
    LocalFlattenedHierarchicalPartition,
)
from mapper.interface import (
    build_base_datagraph,
    build_base_graph_auto,
    build_graph,
    build_hierarchical_graph_from_base,
    build_knn_graph,
    quick_graph,
    quick_graph_old,
)
from mapper.mappergraph import MapperGraph, PartitionGraph, WeightedPartitionGraph
from mapper.matrix import MapperMatrix
from mapper.multiresolution import DisjointPartitionGraph, HierarchicalPartitionGraph
from mapper.neighborgraph import (
    KNNGraph,
    LicenseError,
    NeighborGraph,
    check_key,
    check_license_expiration_soon,
    check_license_manually,
)
from mapper.protocols import AbstractGraph, MultiResolutionGraph

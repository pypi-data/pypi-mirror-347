from typing import Union

import mapper
import mapper.datagraph
import numpy as np
import scipy.sparse as sp

from cobalt.schema.dataset import CobaltDataSubset


def get_group_neighborhood(
    group: CobaltDataSubset,
    graph: Union[
        mapper.HierarchicalPartitionGraph, mapper.datagraph.HierarchicalDataGraph
    ],
    nbhd_size_ratio: float = 2,
    mass_thresh: float = 0.1,
    max_diff_iter: int = 100,
    diffusion_ratio: float = 0.5,
) -> CobaltDataSubset:
    """Finds a neighborhood of points around ``group`` in ``graph``."""
    # for compatibility with old and new mapper interface
    try:
        csr_g = graph.neighbor_graph.graph.csr_graph
    except Exception:
        csr_g = graph.base_graph.csr_graph
    # TODO: drop compatibility for old interface
    # TODO: add support for base graphs with non-singleton nodes

    A = csr_g.get_adjacency_matrix(weight_attr="distance")
    A.data = np.exp(-A.data)
    # this makes A column stochastic
    A = A @ sp.diags(1 / np.maximum(A.sum(axis=0), 1e-9))
    A = A.tocsr()

    source_data: CobaltDataSubset = graph.cobalt_subset
    if len(source_data) != csr_g.n_nodes:
        raise ValueError(
            "Number of nodes in graph does not match number of data points in source data subset."
        )

    subset_mask = group.as_mask_on(source_data).astype(np.float32)
    subset_ind = np.flatnonzero(subset_mask)
    dist = subset_mask.copy()
    orig_mass = len(group)
    for _ in range(max_diff_iter):
        dist = (diffusion_ratio * A @ dist) + (1 - diffusion_ratio) * dist
        new_mass = np.sum(dist[subset_ind])
        if new_mass < mass_thresh * orig_mass:
            break

    thresh_min = dist.min()
    thresh_max = dist.max()
    target_n_points = int(len(group) * nbhd_size_ratio)

    n_bisect_iter = 15
    for _ in range(n_bisect_iter):
        thresh = (thresh_max + thresh_min) / 2
        n_points = np.sum(dist > thresh)
        if n_points < target_n_points:
            thresh_max = thresh
        else:
            thresh_min = thresh

    expanded_subset = source_data.mask(dist > thresh)
    return expanded_subset

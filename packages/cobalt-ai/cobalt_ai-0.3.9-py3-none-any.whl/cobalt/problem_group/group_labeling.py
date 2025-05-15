# Copyright (C) 2023-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.
from __future__ import annotations

from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd

from cobalt.schema import CobaltDataSubset


# TODO: move to method on GroupComparisonStats?
def short_feature_description_string(
    num_stats: pd.DataFrame, cat_stats: pd.DataFrame
) -> str:
    # TODO: pick two features in order based on p-value or something
    if len(num_stats) > 0:
        num_feature_name = num_stats.iloc[0]["feature"]
        feature_mean = num_stats.iloc[0]["mean"]
        complement_mean = num_stats.iloc[0]["complement mean"]
        dir_str = "↑" if feature_mean > complement_mean else "↓"
        num_str = f"{num_feature_name} mean={feature_mean:.2g} ({dir_str})"
    else:
        num_str = ""
    cat_str = ""
    if len(cat_stats) > 0:
        cat_feature_name = cat_stats.iloc[0]["feature"]
        feature_mode = cat_stats.iloc[0]["mode"]
        mode_freq = cat_stats.iloc[0]["frequency (%)"]
        if mode_freq > 50:
            cat_str = f"{cat_feature_name}={feature_mode} ({mode_freq:.1f}%)"
    if len(num_str) > 0:
        summary_str = f"{num_str} | {cat_str}" if len(cat_str) > 0 else num_str
    else:
        summary_str = cat_str

    return summary_str


# TODO: make this a more strongly typed object
# these are dicts of the form
# `{"bucket_sizes": [1,5,3], "bucket_names": ["one", "two", "three"]}`
# they can be passed to the Histogram constructor by spreading:
# `Histogram(**true_class_distribution)`
CategoricalHistogram = Dict[str, Union[List[int], List[str]]]


def get_column_distribution_categorical(
    subset: CobaltDataSubset, col: str
) -> CategoricalHistogram:
    """Calculates the distribution of a categorical column.

    Output is in the format required by the FailureGroupDetails object, to
    support display as a histogram.
    """
    value_counts = subset.select_col(col).value_counts()
    return {
        "bucket_sizes": value_counts.to_list(),
        "bucket_names": value_counts.index.to_list(),
    }


# TODO: include an other category?
def collate_categorical_histograms(
    histograms: List[CategoricalHistogram], max_n_cats: int = 8
):
    """Combines the set of classes for the two histograms in a FailureGroupDetails object."""
    if max_n_cats < 2:
        raise ValueError(
            "max_n_cats must be at least 2 to produce meaningful histograms."
        )
    # TODO: there has to be a nicer way to do this
    # first, get the collection of all bucket names from all histograms
    unique_buckets: set[str] = set()
    for hist in histograms:
        try:
            unique_buckets.update(hist["bucket_names"])
        except KeyError:
            pass
        except AttributeError:
            pass
    new_buckets = list(unique_buckets)

    # add the empty buckets to each histogram, and make sure they're in the same order
    for hist in histograms:
        relabel_buckets(hist, new_buckets)

    # pick the max_n_cats most common categories
    total_counts = np.sum([hist["bucket_sizes"] for hist in histograms], axis=0)
    sorted_indices = np.argsort(total_counts)
    if max_n_cats < len(new_buckets):
        # so that "other" can be added to bring it back up to max_n_cats
        max_n_cats -= 1
    top_indices = np.sort(sorted_indices[-max_n_cats:])
    remaining_indices = sorted_indices[:-max_n_cats]
    new_bucket_names = [new_buckets[i] for i in top_indices]
    # sort by length of the name for display purposes
    # this means the leftmost class names don't stick out as far to the left
    top_indices, new_bucket_names = zip(
        *sorted(zip(top_indices, new_bucket_names), key=lambda x: len(str(x[1])))
    )
    new_bucket_names = list(new_bucket_names)
    if len(remaining_indices) > 0:
        new_bucket_names.append("other")

    for hist in histograms:
        hist["bucket_names"] = list(new_bucket_names)
        new_bucket_sizes = [hist["bucket_sizes"][i] for i in top_indices]
        if len(remaining_indices) > 0:
            other_count = sum(hist["bucket_sizes"][i] for i in remaining_indices)
            new_bucket_sizes.append(other_count)
        hist["bucket_sizes"] = new_bucket_sizes


def relabel_buckets(histogram: Optional[Dict], new_buckets: List):
    """Replaces the set of buckets in a histogram with new labels.

    The bucket size for any label not in the original set will be zero, and
    bucket sizes for previous labels are kept.
    """
    try:
        old_buckets = histogram["bucket_names"]
        old_counts = histogram["bucket_sizes"]
        histogram["bucket_names"] = new_buckets
        new_counts = []
        for bucket in new_buckets:
            if bucket in old_buckets:
                i = old_buckets.index(bucket)
                new_counts.append(old_counts[i])
            else:
                new_counts.append(0)
        histogram["bucket_sizes"] = new_counts
    except KeyError:
        pass
    except TypeError:
        pass

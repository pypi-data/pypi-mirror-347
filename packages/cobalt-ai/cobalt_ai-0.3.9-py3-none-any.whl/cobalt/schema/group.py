# Copyright (C) 2023-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.
from __future__ import annotations

import contextlib
import itertools
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional, Protocol, Sequence, Tuple, Union
from uuid import UUID

import pandas as pd

from cobalt.cobalt_types import GroupType
from cobalt.feature_compare import (
    categorical_feature_compare,
    feature_compare,
    feature_descriptions_from_tables,
    get_categorical_columns,
    get_numerical_features,
    numerical_feature_compare,
)
from cobalt.problem_group.group_labeling import (
    CategoricalHistogram,
    collate_categorical_histograms,
    get_column_distribution_categorical,
    short_feature_description_string,
)
from cobalt.schema.dataset import CobaltDataSubset, DatasetBase
from cobalt.schema.model_metadata import ModelMetadata, ModelTask


@dataclass
class GroupKeywords:
    col: str
    terms: Tuple[str, ...]
    scores: Tuple[float, ...]
    match_rate: Tuple[float, ...]
    params: Dict = field(default_factory=dict)

    def get_keyword_string(
        self, n_keywords: int = 3, min_match_rate: float = 0, delimiter: str = ", "
    ) -> str:
        # TODO: filter keywords for redundancy to make better names
        return delimiter.join(
            itertools.islice(
                (
                    t
                    for t, mr in zip(self.terms, self.match_rate)
                    if t and mr >= min_match_rate
                ),
                n_keywords,
            )
        )

    def __len__(self) -> int:
        return len(self.terms)

    def __repr__(self) -> str:
        return self.get_keyword_string(n_keywords=len(self.terms))


# TODO: refactor schema for better modularity and compatibility


@dataclass
class GroupComparisonStats:
    comparison_group: Union[Literal["all", "rest"], GroupMetadata]
    comparison_group_name: str
    numerical_stats: pd.DataFrame
    categorical_stats: pd.DataFrame
    test: str


@dataclass
class GroupDisplayInfo:
    histograms: Dict[str, CategoricalHistogram] = field(default_factory=dict)
    """A collection of named histograms to display."""

    feature_descriptions: Dict[str, str] = field(default_factory=dict)
    """A collection of feature name => statistical summary pairs."""

    # TODO: this is redundant with GroupMetadata.comparison_stats?
    feature_stat_tables: Dict[str, pd.DataFrame] = field(default_factory=dict)
    """A set of named tables containing feature statistics on this group."""

    # TODO: should these be more specific?
    textual_descriptions: Dict[str, str] = field(default_factory=dict)
    """Named textual descriptions for the group content."""

    visible: bool = True


@dataclass
class GroupMetadata:
    subset: CobaltDataSubset
    """The data points included in this group."""

    name: Optional[str] = None
    """The group's name. Should be unique within a SubsetCollection."""

    metrics: Dict[str, float] = field(default_factory=dict)
    """Relevant numeric metrics for this group."""

    description: Optional[str] = None
    """A short description of the contents of the group."""

    display_info: GroupDisplayInfo = field(default_factory=GroupDisplayInfo)
    """Information to be displayed in the group explorer in the UI."""

    keywords: Dict[str, GroupKeywords] = field(default_factory=dict)
    """Distinctive keywords found in text columns in the group."""

    comparison_stats: Dict[str, GroupComparisonStats] = field(default_factory=dict)
    """Results of statistical tests comparing this group with others."""

    group_type: GroupType = GroupType.any
    """Describes the semantic meaning of the group in context."""

    # TODO: should metrics be grouped by model, or at least have the option?

    other_fields: Dict[str, Any] = field(default_factory=dict)

    def compute_comparison_stats(
        self,
        comparison_group: Union[Literal["all", "rest"], GroupMetadata],
        omit_columns: Optional[Sequence[str]] = None,
        set_description_string: bool = True,
        set_display_info: bool = True,
        test: Literal["t-test", "perm"] = "t-test",
    ):
        if comparison_group == "all":
            comparison_group_name = "all"
            comparison_subset: DatasetBase = self.subset.source_dataset
        elif comparison_group == "rest":
            comparison_group_name = "rest"
            comparison_subset = self.subset.complement()
        else:
            comparison_group_name = comparison_group.name
            comparison_subset = comparison_group.subset

        if omit_columns is not None:
            numerical_features = get_numerical_features(self.subset.source_dataset.df)
            numerical_features = list(set(numerical_features).difference(omit_columns))
            num_stats = numerical_feature_compare(
                self.subset, comparison_subset, numerical_features, test=test
            )
            categorical_features = get_categorical_columns(self.subset.source_dataset)
            categorical_features = list(
                set(categorical_features).difference(omit_columns)
            )
            cat_stats = categorical_feature_compare(
                self.subset, comparison_subset, categorical_features
            )
        else:
            num_stats, cat_stats = feature_compare(self.subset, comparison_subset)
        self.comparison_stats[comparison_group_name] = GroupComparisonStats(
            comparison_group=comparison_group,
            comparison_group_name=comparison_group_name,
            numerical_stats=num_stats,
            categorical_stats=cat_stats,
            test=test,
        )

        if set_description_string:
            self.description = short_feature_description_string(
                num_stats.rename(
                    {"mean A": "mean", "mean B": "complement mean"}, axis=1
                ),
                cat_stats,
            )

        if set_display_info and comparison_group_name == "rest":
            num_stats = (
                num_stats[num_stats["p-value"] <= 0.001]
                .iloc[: min(3, len(num_stats)), :]
                .copy()
                .rename({"mean A": "mean", "mean B": "complement mean"}, axis=1)
            )
            cat_stats = (
                cat_stats[
                    (cat_stats["p-value"] <= 0.001) & (cat_stats["frequency (%)"] >= 50)
                ]
                .iloc[: min(3, len(cat_stats)), :]
                .copy()
            )
            cat_stats["complement frequency (%)"] = [
                (comparison_subset.select_col(row["feature"]) == row["mode"]).mean()
                * 100
                for _, row in cat_stats.iterrows()
            ]
            self.display_info.feature_descriptions = feature_descriptions_from_tables(
                num_stats, cat_stats
            )
        # TODO: should this return something?

    # TODO: add color map for histogram.
    def add_categorical_histograms_for_columns(
        self,
        columns: Sequence[str],
        histogram_titles: Sequence[str],
        collate_categories: bool = False,
        max_n_cats: int = 6,
    ):
        histograms = [
            get_column_distribution_categorical(self.subset, c) for c in columns
        ]
        if collate_categories:
            collate_categorical_histograms(histograms, max_n_cats=max_n_cats)
        else:
            for h in histograms:
                collate_categorical_histograms([h], max_n_cats=max_n_cats)

        for title, hist in zip(histogram_titles, histograms):
            self.display_info.histograms[title] = hist

    def add_model_data_histograms(self, model: ModelMetadata, max_n_classes: int = 6):
        if model.task != ModelTask.classification:
            return
        columns = []
        titles = []
        if model.outcome_column:
            columns.append(model.outcome_column)
            titles.append(f"Label Distribution ({model.outcome_column})")
        if model.prediction_column:
            columns.append(model.prediction_column)
            titles.append(f"Prediction Distribution ({model.prediction_column})")
        if len(columns) == 0:
            return
        self.add_categorical_histograms_for_columns(
            columns, titles, collate_categories=True, max_n_cats=max_n_classes
        )

    def add_group_description_from_keywords(
        self, keyword_column: str, include_col_name_in_description: bool = False
    ):
        keyword_string = self.keywords[keyword_column].get_keyword_string(
            delimiter=" | "
        )
        prefix = (
            f"Keywords ({keyword_column})"
            if include_col_name_in_description
            else "Keywords"
        )
        self.description = f"{prefix}: {keyword_string}"

    def __getattr__(self, name):
        try:
            return self.other_fields[name]
        except KeyError:
            raise AttributeError(
                f"{self.__class__.__name__!r} object has no attribute {name!r}"
            ) from None

    def __repr__(self) -> str:
        return f"GroupMetadata(name={self.name!r}, keywords={self.keywords!r})"


class Group(Protocol):
    name: Optional[str]
    subset: CobaltDataSubset
    summary: str
    metrics: Dict[str, float]
    group_details: GroupDisplayInfo
    visible: bool = True
    run_id: Optional[UUID] = None


@dataclass
class ProblemGroup(GroupMetadata, Group):
    """A group representing a problem with a model."""

    problem_description: str = ""
    """A brief description of the problem."""

    severity: float = 1.0
    """A score representing the degree of seriousness of the problem.

    Used to sort a collection of groups. Typically corresponds to the value of a
    performance metric on the group, and in general is only comparable within
    the result set of a single algorithm run.
    """

    primary_metric: Optional[str] = None
    """The main metric used to evaluate this group."""

    visible: bool = True
    run_id: Optional[UUID] = None

    @property
    def group_details(self) -> GroupDisplayInfo:
        return self.display_info

    @group_details.setter
    def group_details(self, val):
        self.display_info = val

    @property
    def summary(self) -> str:
        return self.description or ""

    @summary.setter
    def summary(self, val):
        self.description = val

    def __post_init__(self):
        if self.primary_metric is None:
            # assume the first metric in the dict is the main one to use
            with contextlib.suppress(StopIteration):
                self.primary_metric = next(iter(self.metrics.keys()))
        if self.problem_description == "" and self.primary_metric:
            self.problem_description = (
                f"{len(self.subset)} points | "
                f"{self.primary_metric}: {self.metrics[self.primary_metric]:.3g}"
            )

    # This is not a strict __repr__() method since it can't be used to reinstantiate the object
    # but that wouldn't be easily possible anyway
    # We use __repr__() instead of __str__() so that it controls the default
    # rendering when a ProblemGroup is in the output of a Jupyter cell.
    def __repr__(self):
        return (
            f"ProblemGroup(name={self.name!r}, "
            f"subset={self.subset.__class__.__name__}(n_points={len(self.subset)}), "
            f"problem_description={self.problem_description!r}, "
            f"metrics={self.metrics})"
        )


@dataclass
class Cluster(Group):
    name: str
    subset: CobaltDataSubset
    problem_description: str = ""
    summary: str = ""
    metrics: Dict[str, float] = field(default_factory=dict)
    group_details: GroupDisplayInfo = field(default_factory=GroupDisplayInfo)
    group_type: GroupType = GroupType.cluster
    visible: bool = True
    run_id: Optional[UUID] = None

    def __repr__(self):
        return f"Cluster(subset={self.subset.__class__.__name__}(n_points={len(self.subset)}))"

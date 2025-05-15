# Copyright (C) 2023-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

from __future__ import annotations

import copy
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

import pandas as pd

from cobalt.cobalt_types import GroupType, RunType
from cobalt.schema.dataset import CobaltDataset, CobaltDataSubset
from cobalt.schema.group import GroupMetadata, ProblemGroup
from cobalt.schema.group_collection import GroupCollection
from cobalt.schema.model_metadata import ModelMetadata


class GetGroupsFormat(Enum):
    as_dict = "dict"
    as_list = "list"
    as_batch = "batch"


class GroupResultsCollection(GroupCollection):
    """Contains the results of a group analysis on a dataset."""

    name: str
    """A name for the collection of results. May be referred to as a "run
    name", since it corresponds to a particular run of an algorithm.
    """

    source_data: CobaltDataSubset
    """The data(sub)set used for the analysis, as a CobaltDataSubset object."""

    groups: List[ProblemGroup]
    """A list of objects containing the discovered groups, with metadata (e.g.
    descriptions, model performance metrics) alongside each group.
    """

    group_type: GroupType
    """What each group in the collection represents, e.g. a failure group or a cluster."""

    algorithm: str
    """The algorithm used to produce the groups."""

    params: Dict
    """Parameters passed to the group-finding algorithm."""

    run_type: RunType
    """Whether the algorithm was run manually by the user or automatically by Cobalt."""

    visible: bool
    """Whether the groups should be displayed in the UI."""

    run_id: UUID
    """A unique ID for this collection of groups."""

    def __init__(
        self,
        name: str,
        run_type: RunType,
        source_data: CobaltDataSubset,
        group_type: GroupType,
        algorithm: str,
        params: dict,
        groups=None,
        visible: bool = True,
        run_id: Optional[UUID] = None,
    ) -> None:
        self._groups: List[ProblemGroup] = groups if groups else []
        group_metadata = [
            GroupMetadata(
                subset=g.subset,
                name=g.name,
                metrics=g.metrics,
                description=g.summary,
                display_info=g.group_details,
                group_type=group_type,
            )
            for g in self._groups
        ]
        indices = [g.subset.indices for g in group_metadata]
        source_dataset = (
            source_data
            if isinstance(source_data, CobaltDataset)
            else source_data.source_dataset
        )
        super().__init__(source_dataset, indices, name=name, group_type=group_type)
        self._subset_objects = [g.subset for g in group_metadata]
        self._group_objects = group_metadata

        self.run_id = run_id if run_id else uuid4()
        self.source_data = source_data
        self.type = run_type
        self.algorithm = algorithm
        self.params = params
        self.visible = visible

    @property
    def groups(self) -> List[ProblemGroup]:
        return [
            ProblemGroup(
                name=g.name or f"{self.name}/{i}",
                subset=g.subset,
                description=g.description or "",
                problem_description=g.other_fields.get("problem_description", ""),
                metrics=g.metrics,
                display_info=g.display_info,
                group_type=g.group_type,
                visible=g.display_info.visible,
                run_id=self.run_id,
            )
            for i, g in enumerate(self.metadata)
        ]

    @property
    def raw_groups(self) -> List[CobaltDataSubset]:
        """The groups as a list of CobaltDataSubset objects.

        Omits the descriptive metadata.
        """
        return list(self)

    def _get_default_model(self) -> Optional[ModelMetadata]:
        if self.group_type == GroupType.failure:
            return self.params.get("model")
        else:
            return None

    def _get_production_subset(self) -> Optional[CobaltDataSubset]:
        if self.group_type == GroupType.drift:
            return self.params.get("prod")
        else:
            return None

    def summary(
        self,
        model: Optional[ModelMetadata] = None,
        production_subset: Optional[CobaltDataSubset] = None,
    ) -> pd.DataFrame:
        """Create a tabular summary of the groups in this collection.

        Args:
            model: A ModelMetadata object whose performance metrics will be
                computed for the groups.
            production_subset: If provided, will calculate the fraction of data
                points in each group that fall in this subset.
        """
        table_rows = []
        model = model or self._get_default_model()
        production_subset = production_subset or self._get_production_subset()
        for group in self.groups:
            subset = group.subset
            size = len(subset)
            row = {
                "Group Name": group.name,
                "Size": size,
            }
            row["Description"] = group.summary
            row.update(group.metrics)
            if model:
                row.update(model.overall_performance_metrics(group.subset))
            if production_subset:
                prod_count = len(subset.intersect(production_subset))
                row["Production Frequency"] = prod_count / size

            table_rows.append(row)
        return pd.DataFrame(table_rows)

    def filter_by_severity(self, min_severity: float) -> GroupResultsCollection:
        return GroupResultsCollection(
            self.name,
            self.run_type,
            self.source_data,
            self.group_type,
            self.algorithm,
            params=self.params,
            groups=[g for g in self.groups if g.severity >= min_severity],
            visible=self.visible,
            run_id=self.run_id,  # ??
        )

    def __eq__(self, other):
        """Add source_data comparison if needed."""
        if not isinstance(other, GroupResultsCollection):
            return NotImplemented

        return all(
            [
                self.name == other.name,
                self.type == other.type,
                self.group_type == other.group_type,
                self.algorithm == other.algorithm,
                self.params == other.params,
                self.groups == other.groups,
                self.visible == other.visible,
            ]
        )

    def __repr__(self):
        return (
            f"GroupResultsCollection(n_groups={len(self.groups)}, "
            f"group_type={self.group_type.name}, "
            f"algorithm={self.algorithm}, groups={self.groups})"
        )

    def _repr_html_(self):
        """Defines representation in an IPython output cell."""
        table_html = self.summary()._repr_html_()
        n_groups = len(self.groups)
        n_groups_str = (
            f"{n_groups} {self.group_type.value}s"
            if n_groups != 1
            else f"1 {self.group_type.value}"
        )
        return f"<h4>{n_groups_str}</h4> {table_html}"


class GroupResultsCollectionRepository:
    def __init__(self) -> None:
        self.runs: Dict[str, GroupResultsCollection] = {}

    def get_run(self, name):
        return self.runs.get(name)

    def build_run(
        self,
        run_name: Optional[str],
        run_type,
        groups,
        algorithm,
        group_type,
        source_data,
        params,
        run_id=None,
        visible=True,
    ) -> GroupResultsCollection:
        run = GroupResultsCollection(
            run_id=run_id if run_id else uuid4(),
            name=run_name if run_name else self.new_run_name(),
            run_type=run_type,
            groups=groups,
            algorithm=algorithm,
            group_type=group_type,
            source_data=source_data,
            params=params,
            visible=visible,
        )
        for group in run.groups:
            group.run_id = run.run_id
        self.add_run(run)
        return run

    def add_run(self, run):
        self.runs[run.name] = run

    def get_group_by_id(self, group_id):
        for run in self.runs:
            for group in run.groups:
                if group.id == group_id:
                    return group
        return self.runs

    def get_runs(
        self,
        run_name: Optional[str] = None,
        group_type: Optional[GroupType] = None,
        run_type: Optional[RunType] = None,
        run_visible: Optional[bool] = None,
    ) -> Dict[str, GroupResultsCollection]:
        """Retrieve runs satisfying given criteria.

        If no arguments are provided, return all runs.

        Args:
            run_name: Name of specific run to retrieve
            group_type: Include only groups of specific type
            run_type: Manual or Automatic
            run_visible: Filter out runs which are hidden/not hidden
        """
        result_runs = [copy.copy(run) for run in self.runs.values()]
        if run_name is not None:
            result_runs = [self.runs[run_name]]

        if group_type:
            result_runs = self.filter_groups_by_group_type(
                group_type=group_type, runs=result_runs
            )

        if run_type:
            result_runs = self.filter_out_by_run_type(
                runs=result_runs, run_type=run_type
            )

        if run_visible is not None:
            result_runs = self.filter_out_runs_by_visibility(
                runs=result_runs, visible=run_visible
            )
        return {run.name: run for run in result_runs}

    def filter_groups_by_group_type(self, runs, group_type: GroupType):
        result = [run for run in runs if run.group_type == group_type]
        return result

    def filter_out_by_run_type(self, runs, run_type: str):
        result = [run for run in runs if run.type == RunType(run_type)]
        return result

    def is_name_unique_problem_groups(self, run_name: str, group_name: str):
        run = self.runs[run_name]
        for group in run.groups:
            if group.name is not None and group.name == group_name:
                return False
        return True

    def filter_out_runs_by_visibility(self, runs, visible=True):
        result = [run for run in runs if run.visible == visible]
        return result

    def new_run_name(self):
        return f"run_{len(self.runs)}"

    def get_runs_count(self):
        return len(self.runs)

# Copyright (C) 2023-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

from __future__ import annotations

from typing import TYPE_CHECKING, List

import ipyvuetify as v

from cobalt.config import handle_cb_exceptions
from cobalt.event_bus import EventBusController
from cobalt.feature_compare import feature_compare
from cobalt.groups.failure_groups import convert_group_to_dict
from cobalt.groups.group_details import GroupDetails
from cobalt.groups.groups_ui import GroupDisplay, GroupSaveButton
from cobalt.schema import CobaltDataSubset
from cobalt.schema.group import ProblemGroup
from cobalt.selection_details import SelectionDetails
from cobalt.selection_manager import SelectionManager
from cobalt.table.table_view import TableView
from cobalt.ui_utils import with_tooltip
from cobalt.visualization import EmbeddingVisualization
from cobalt.widgets import Button, Select
from cobalt.widgets.progress_bar import ProgressBar

if TYPE_CHECKING:
    from cobalt.workspace import Workspace

CURRENT_GRAPH_NEIGHBORS = "current_graph_neighbors"
CURRENT_SELECTION = "current_selection"
ALL = "all"
REST = "rest"

test_name_to_param = {
    "t-test": "t-test",
    "KS test": "ks-test",
    "Wilcoxon rank-sum test": "rank-sum",
    "permutation t-test": "perm",
}

group_to_compare_display_names = {
    CURRENT_GRAPH_NEIGHBORS: "Neighbors in current graph",
    CURRENT_SELECTION: "Current graph selection",
    ALL: "All data points",
    REST: "Rest of data points",
}


class GroupsComparison(v.Flex):
    def __init__(
        self,
        dataselector: SelectionManager,
        visualization: EmbeddingVisualization,
        workspace: Workspace,
    ):
        # Initial params
        self.workspace = workspace
        self.state = workspace.state
        self.dataselector = dataselector
        self.visualization = visualization
        self.selected_group_name = None
        self.selected_group_data_points = None
        self.group_to_compare_name = None
        self.is_current_selection_disabled = False

        # Bindings
        self.bind_selection_manager()

        # Event listeners
        self.dataselector.on_comparison_group_select(self.update_comparison_group)
        group_event_bus = EventBusController.get_group_event_bus(
            self.state.workspace_id
        )
        run_event_bus = EventBusController.get_run_event_bus(self.state.workspace_id)

        group_event_bus.add_callback(self.update_group_compare_items)
        run_event_bus.add_callback(self.update_group_details)
        self.visualization.on_graph_update(self.update_group_compare_items)

        # Data preparation
        self.failure_groups = self.get_failure_groups()
        self.failure_groups_dict = convert_group_to_dict(self.failure_groups)
        self.group_details = GroupDetails(dataselector, items=self.failure_groups_dict)
        self.group_display = GroupDisplay(dataselector, visualization, self.state)
        self.selection_details = SelectionDetails(dataselector, self.state)
        self.save_button = GroupSaveButton(
            self.dataselector, self.state, group_display=self.group_display
        )
        self.save_button.on_event("click", self.save_button.update_data_points)
        self.number_of_points = self.selection_details.number_of_points

        # UI components initialization
        self.initialize_ui()

        # Widget setup
        self.group_compare_with.on_event("change", self.update_comparison_results_cb)
        self.statistical_test_select.on_event(
            "change", self.update_comparison_results_cb
        )

        super().__init__(
            children=[
                v.Layout(
                    column=True,
                    children=[
                        self.groups_header,
                        self.comparison_selects,
                        self.comparison_results,
                        self.group_details,
                    ],
                    class_="pa-4",
                    style_="width: 100%",
                )
            ],
        )

    def get_failure_groups(self) -> List[ProblemGroup]:
        return self.workspace._get_displayed_groups()

    def initialize_ui(self):
        self.clear_selection_button = Button(
            icon=True,
            children=[
                v.Icon(
                    children=["mdi mdi-arrow-left"],
                    color="primary",
                )
            ],
            style_="margin-left: -8px",
        )
        self.clear_selection_button.on_event(
            "click", self.on_clear_selection_button_click
        )

        self.groups_header = v.Flex(
            children=[self.clear_selection_button, self.save_button],
            class_="d-flex justify-space-between align-center",
            style_="width: 100%;",
        )

        self.selected_group_name_widget = v.Text(
            children="",
            style_="font-size: 20px;",
        )

        self.selected_group_data_points_widget = v.Flex(
            children="",
            style_="font-size: 13px;",
        )

        self.group_compare_with = Select(
            label="Compare with",
            v_model=None,
            attach=True,
            items=self.get_group_compare_items(),
            class_="elevation-1",
            style_="max-width: 200px",
            disabled=False,
        )

        self.statistical_test_select = Select(
            label="Statistical test",
            v_model="t-test",
            attach=True,
            items=list(test_name_to_param.keys()),
            class_="elevation-1",
            style_="max-width: 200px",
            hint="Test to compare values of numerical columns",
            persistent_hint=True,
            disabled=False,
        )

        self.spinner = ProgressBar(width=4, size=25, indeterminate=True)
        self.spinner_tooltip = with_tooltip(
            self.spinner,
            "Running statistical tests. Interrupt Jupyter kernel to stop.",
            styles="margin: 0 5px;",
        )
        self.spinner.hide()

        self.table_widget = v.Flex(class_="d-flex flex-wrap", style_="gap: 40px")

        self.close_comparison_button = Button(
            icon=True,
            children=[v.Icon(children=["mdi mdi-close"], color="primary")],
        )
        self.close_comparison_button.on_event(
            "click", self.on_close_comparison_button_click
        )

        self.close_comparison_button_with_tooltip = with_tooltip(
            self.close_comparison_button, "Clear Comparison"
        )

        self.comparison_title = v.Flex(
            children=[],
            class_="d-flex justify-space-between align-center",
            style_="font-size: 14px;",
        )

        self.comparison_selects = v.Layout(
            children=[
                v.Flex(
                    children=[
                        v.Layout(
                            children=[
                                self.selected_group_name_widget,
                                self.selected_group_data_points_widget,
                            ],
                            column=True,
                        ),
                        self.spinner_tooltip,
                        self.group_compare_with,
                        self.statistical_test_select,
                    ],
                    class_="d-flex justify-space-between align-center flex-wrap",
                    style_="width: 100%;",
                ),
            ],
            column=True,
        )

        self.comparison_results = v.Flex(children=[], class_="mt-2")

        self.list_box = v.List(
            dense=True,
            children=[self.group_display.list_item_group],
            class_="overflow-y-auto",
        )

    @handle_cb_exceptions
    def on_selection_source_change(self, source):
        if source != "Graph":
            self.save_button.disabled = True
            self.is_current_selection_disabled = True
        else:
            self.save_button.disabled = False
            self.is_current_selection_disabled = False
        self.update_group_compare_items()

    def bind_selection_manager(self):
        self.dataselector.on_comparison_group_select(self.update_comparison_group)
        self.selection_details = SelectionDetails(
            self.dataselector, self.state, self.on_selection_source_change
        )
        self.dataselector.on_graph_select(
            self.update_current_selection_comparison_from_graph
        )
        self.dataselector.on_group_select(self.on_close_comparison_button_click)

    @handle_cb_exceptions
    def update_current_selection_comparison_from_graph(self, *_):
        if self.group_to_compare_name == CURRENT_SELECTION and self.selected_group_name:
            # The comparison of groups closes if the user clears
            # the selection on the graph or selects all nodes.
            if len(self.dataselector.graph_selection) == len(
                self.visualization.source_data
            ):
                self.on_close_comparison_button_click()
            else:
                self.update_comparison_results_cb()

    @handle_cb_exceptions
    def update_comparison_group(self, selected_item):
        self.comparison_results.children = []

        self.selected_group_name = selected_item["group_id"]
        user_groups_info = self.state.get_groups_info()

        if self.selected_group_name in user_groups_info:
            group_size = user_groups_info.get(self.selected_group_name, None)
        else:
            failure_groups_index = {
                group["group_id"]: group for group in self.failure_groups_dict
            }
            failure_group_info = failure_groups_index.get(self.selected_group_name, {})
            group_size = failure_group_info.get("group_size", None)

        self.selected_group_data_points = group_size

        self.selected_group_name_widget.children = self.selected_group_name
        self.selected_group_data_points_widget.children = (
            f"data points: {self.selected_group_data_points}"
        )

        self.group_details.update_comparison_group(selected_item)
        self.update_group_compare_items()

    @handle_cb_exceptions
    def on_clear_selection_button_click(self, *args):
        self.selected_group_name = None
        self.selected_group_data_points = None
        self.group_to_compare_name = None
        if hasattr(self.visualization, "landscape"):
            self.visualization.landscape.graph_viewer.selected_points = []

        self.dataselector.graph_selection = None
        del self.dataselector.graph_selection

        self.dataselector.graph_selection = self.state.dataset.subset([])
        self.dataselector.set_group_selection(None)
        self.dataselector.trigger_clear_selection_listeners()

    @handle_cb_exceptions
    def on_close_comparison_button_click(self, *args):
        self.group_details.show_details()
        self.group_compare_with.v_model = None
        self.comparison_results.children = []
        self.group_to_compare_name = None

    def get_group_data_by_name(self, group_name: str) -> CobaltDataSubset:
        group_subset = None
        try:
            # try to find a group in user groups
            group_subset = self.state.get_group(group_name)
        except KeyError:
            # this is a failure group
            for f_group in self.failure_groups:
                if f_group.name == group_name:
                    group_subset = f_group.subset
                    break
        if not group_subset:
            raise ValueError(f"Group {group_name} doesn't exist")
        return group_subset

    @handle_cb_exceptions
    def update_comparison_results_cb(self, *_):
        self.group_details.hide_details()
        self.group_to_compare_name = self.group_compare_with.v_model

        first_group = self.get_group_data_by_name(self.selected_group_name)

        if self.group_to_compare_name == CURRENT_SELECTION:
            second_group = self.dataselector.graph_selection
        elif self.group_to_compare_name == ALL:
            second_group = self.dataselector.dataset
        elif self.group_to_compare_name == REST:
            second_group = first_group.complement()
        elif self.group_to_compare_name == CURRENT_GRAPH_NEIGHBORS:
            graph = self.visualization.landscape.graph
            second_group = self.workspace.get_group_neighbors(first_group, graph)
        else:
            second_group = self.get_group_data_by_name(self.group_to_compare_name)

        test_name = self.statistical_test_select.v_model
        test_param = test_name_to_param[test_name]

        try:
            self.spinner.show()
            self.update_comparison_results(first_group, second_group, test_param)
        finally:
            self.spinner.hide()

    def update_comparison_results(
        self, first_group: CobaltDataSubset, second_group: CobaltDataSubset, test
    ):
        stats_df, c_stats_df = feature_compare(
            first_group, second_group, numerical_test=test
        )
        self.table_widget.children = [
            v.Layout(
                children=[
                    v.Html(tag="span", children="Numerical features"),
                    TableView(
                        stats_df, numeric_format="{:.3g}", style="margin: 0 -16px"
                    ),
                ],
                class_="flex-column",
            ),
            v.Layout(
                children=[
                    v.Html(tag="span", children="Categorical features"),
                    TableView(
                        c_stats_df, numeric_format="{:.3g}", style="margin: 0 -16px"
                    ),
                ],
                class_="flex-column",
            ),
        ]
        self.comparison_results.children = [
            self.comparison_title,
            v.Html(tag="br"),
            self.table_widget,
        ]
        self.update_comparison_title()

    def update_comparison_title(self):
        self.comparison_title.children = [
            v.Html(
                tag="span",
                children=[
                    "Comparing ",
                    v.Html(tag="b", children=[self.selected_group_name]),
                    " vs ",
                    v.Html(
                        tag="b",
                        children=[
                            group_to_compare_display_names.get(
                                self.group_to_compare_name, self.group_to_compare_name
                            )
                        ],
                    ),
                ],
            ),
            self.close_comparison_button_with_tooltip,
        ]

    def get_group_compare_items(self):
        user_group_names = list(self.state.get_groups().keys())

        selected_group_is_subset_of_current_graph = False
        try:
            selected_group = self.get_group_data_by_name(self.selected_group_name)
            if self.visualization.source_data is not None:
                graph_source_data = self.visualization.source_data
                if graph_source_data.intersection_size(selected_group) == len(
                    selected_group
                ):
                    selected_group_is_subset_of_current_graph = True
        except ValueError:
            pass

        items = [
            {
                "text": "All",
                "value": "all",
            },
            {
                "text": "Rest",
                "value": "rest",
            },
            {
                "text": "Current selection",
                "value": CURRENT_SELECTION,
                "disabled": self.is_current_selection_disabled,
            },
            {
                "text": "Neighbors in current graph",
                "value": CURRENT_GRAPH_NEIGHBORS,
                "disabled": not selected_group_is_subset_of_current_graph,
            },
        ]

        if user_group_names:
            items.append(
                {
                    "header": "USER CREATED GROUPS",
                }
            )
            for group_name in user_group_names:
                items.append(
                    {
                        "text": group_name,
                        "value": group_name,
                        "disabled": group_name == self.selected_group_name,
                    }
                )
        if len(self.failure_groups_dict) > 0:
            items.append({"header": "FAILURE GROUPS"})
            items.extend(
                [
                    {
                        "text": fg["group_id"],
                        "value": fg["group_id"],
                        "disabled": fg["group_id"] == self.selected_group_name,
                    }
                    for fg in self.failure_groups_dict
                ]
            )

        return items

    @handle_cb_exceptions
    def update_group_compare_items(self):
        self.group_compare_with.items = self.get_group_compare_items()

    @handle_cb_exceptions
    def update_group_details(self):
        self.failure_groups = self.get_failure_groups()
        self.failure_groups_dict = convert_group_to_dict(self.failure_groups)
        self.group_details.update_items(self.failure_groups_dict)
        self.update_group_compare_items()

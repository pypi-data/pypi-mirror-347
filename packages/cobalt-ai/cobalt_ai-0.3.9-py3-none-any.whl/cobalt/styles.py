# Copyright (C) 2023-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.
group_container_style_list = (
    "min-width: 340px; ",
    "max-width: 100%; ",
    "min-height: 456px; ",
    "border: 1px solid #E0E0E0;",
    "border-radius: 4px;",
    "overflow-y: auto;",
    "flex: 3;",
    "max-height: 456px;",
)

DEFAULT_GROUP_CONTAINER_STYLES = "".join(group_container_style_list)

NO_MAX_HEIGHT_GROUP_CONTAINER_STYLES = (
    "".join(group_container_style_list[:-1]) + "max-height:748px;"
)

DEFAULT_COLORING_LEGEND_STYLES = "max-height: 400px; z-index: 2;"
EXPANDED_COLORING_LEGEND_STYLES = "max-height: 700px; z-index: 2;"

LIGHT_GREY_BORDER = "border: 1px solid #E0E0E0"

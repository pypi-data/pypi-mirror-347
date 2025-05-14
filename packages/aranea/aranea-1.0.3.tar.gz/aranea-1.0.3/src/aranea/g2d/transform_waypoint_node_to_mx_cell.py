""" 
Module for transforming WaypointNode objects from the JSON graph model into MxCellShape objects
for the drawio XML format. The transformation handles waypoint nodes with their styling.
"""

from uuid import UUID

from aranea.models.graph_model import WaypointNode
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import MxCellShape, MxCellStyle, MxGeometryShape

DEFAULT_WAYPOINT_DIMENSION = 20


def transform_waypoint_node_to_mx_cell(
    uuid: UUID, node: WaypointNode, style_config: StyleConfig
) -> list[MxCellShape]:
    """
    Transform a WaypointNode object into an MxCellShape object for the drawio XML format.
    """
    mx_cell_style: MxCellStyle = style_config.get_mx_cell_style(node_type=node.type)

    mx_geometry: MxGeometryShape = MxGeometryShape(
        attr_x=node.xRemFactor * style_config.rem_size - DEFAULT_WAYPOINT_DIMENSION / 2,
        attr_y=node.yRemFactor * style_config.rem_size - DEFAULT_WAYPOINT_DIMENSION / 2,
        attr_height=DEFAULT_WAYPOINT_DIMENSION,
        attr_width=DEFAULT_WAYPOINT_DIMENSION,
    )

    mx_cell_shape: MxCellShape = MxCellShape(
        attr_id=uuid,
        attr_style=mx_cell_style.to_semicolon_string(),
        geometry=mx_geometry,
    )

    return [mx_cell_shape]

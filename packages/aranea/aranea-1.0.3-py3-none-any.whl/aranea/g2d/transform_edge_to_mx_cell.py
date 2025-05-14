"""
This module provides a model transformation (Graph-Model->XML-Model) for a single edge.
"""

from uuid import uuid4

from aranea.models.graph_model import (Edge, NetworkDFFClassification,
                                       ProtocolType, TextOrientation)
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import MxCellEdge, MxCellStyle, MxGeometryEdge


def get_source_attachment_point_style_string(
    source_attachment_point_x: float,
    source_attachment_point_y: float,
) -> str:
    """
    Function to generate a source attachment point style string.

    :param source_attachment_point_x: The x coordinate of the source attachment point.
    :type: float
    :param source_attachment_point_y: The y coordinate of the source attachment point.
    :type: float
    :return: The source attachment point style string.
    :rtype: str
    """
    return f"exitX={source_attachment_point_x};exitY={source_attachment_point_y}"


def get_target_attachment_point_style_string(
    target_attachment_point_x: float,
    target_attachment_point_y: float,
) -> str:
    """
    Function to generate a target attachment point style string.

    :param target_attachment_point_x: The x coordinate of the target attachment point.
    :type: float
    :param target_attachment_point_y: The y coordinate of the target attachment point.
    :type: float
    :return: The target attachment point style string.
    :rtype: str
    """
    return f"entryX={target_attachment_point_x};entryY={target_attachment_point_y}"


def transform_edge_to_mx_cell(
    edge: Edge,
    protocol_type: ProtocolType,
    style_config: StyleConfig,
    dff_classification: NetworkDFFClassification | None = None,
) -> list[MxCellEdge]:
    """
    Function to transform an edge to a MxCellEdge.

    :param edge: The edge to transform.
    :type: Edge
    :param protocol_type: The protocol type of the edge.
    :type: ProtocolType
    :param style_config: The StyleConfig to use for the transformation.
    :type: StyleConfig
    :param dff_classification: The DFF classification of the network.
    :type: NetworkDFFClassification | None

    :return: The list of MxCellEdges.
    :rtype: list[MxCellEdge]
    """
    mx_cell_style: MxCellStyle = style_config.get_mx_cell_style(
        protocol_type=protocol_type, network_dff_classification=dff_classification
    )
    if text := edge.text:
        mx_cell_style.fontSize = text[2] * style_config.rem_size
        mx_cell_style.horizontal = text[1] == TextOrientation.HORIZONTAL
        attr_value_local = text[0]
    else:
        attr_value_local = None

    if edge.sourceAttachmentPointX:
        mx_cell_style.exitX = edge.sourceAttachmentPointX
    else:
        mx_cell_style.exitX = 0.0
    if edge.sourceAttachmentPointY:
        mx_cell_style.exitY = edge.sourceAttachmentPointY
    else:
        mx_cell_style.exitY = 0.0

    if edge.targetAttachmentPointX:
        mx_cell_style.entryX = edge.targetAttachmentPointX
    else:
        mx_cell_style.entryX = 0.0
    if edge.targetAttachmentPointY:
        mx_cell_style.entryY = edge.targetAttachmentPointY
    else:
        mx_cell_style.entryY = 0.0

    mx_geometry: MxGeometryEdge = MxGeometryEdge()

    mx_cell_edge: MxCellEdge = MxCellEdge(
        attr_id=uuid4(),
        attr_value=attr_value_local,
        attr_style=mx_cell_style.to_semicolon_string(),
        attr_source=edge.sourceId,
        attr_target=edge.targetId,
        geometry=mx_geometry,
    )

    return [mx_cell_edge]

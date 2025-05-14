"""
Module for providing a default style config.
"""

from pydantic_extra_types.color import Color

from aranea.models.graph_model import (EcuClassificationName, NodeType,
                                       ProtocolTypeName)
from aranea.models.style_config_model import (Align, Arrow, FillStyle,
                                              JumpStyle, Perimeter, Shape,
                                              StyleAttributes, StyleConfig,
                                              VerticalAlign, WhiteSpace)


def get_default_style_config() -> StyleConfig:
    """
    Function that returns a default style config.
    :return: StyleConfig
    """
    return StyleConfig(
        rem_size=12.0,
        node_type_style_attributes={
            NodeType.COMPONENT: StyleAttributes(
                shape=Shape.RECTANGLE,
                fill_color=Color("#FFFFFF"),
                fill_style=FillStyle.SOLID,
                stroke_color=Color("#000000"),
                stroke_width=1,
                white_space=WhiteSpace.WRAP,
            ),
            NodeType.XOR: StyleAttributes(
                shape=Shape.ELLIPSE,
                fill_color=Color("#CCCCCC"),
                fill_style=FillStyle.SOLID,
                stroke_color=Color("#000000"),
                stroke_width=1,
                white_space=WhiteSpace.WRAP,
            ),
            NodeType.TEXT: StyleAttributes(
                shape=Shape.TEXT,
                resizable=True,
                fill_color="NONE",
                stroke_color="NONE",
                autosize=True,
                align=Align.RIGHT,
                vertical_align=VerticalAlign.MIDDLE,
                white_space=WhiteSpace.WRAP,
            ),
            NodeType.WAYPOINT: StyleAttributes(
                shape=Shape.WAYPOINT,
                fill_color="NONE",
                fill_style=FillStyle.SOLID,
                resizable=False,
                rotatable=False,
                size=6,
                perimeter=Perimeter.CENTER,
            ),
        },
        node_classification_style_attributes={
            EcuClassificationName.ECU: StyleAttributes(
                rounded=True,
            ),
            EcuClassificationName.NEW_ECU: StyleAttributes(
                rounded=True,
                fill_color=Color("#708E3F"),
                fill_style=FillStyle.HATCH,
            ),
            EcuClassificationName.ECU_ONLY_IN_BR: StyleAttributes(
                rounded=True,
                fill_color=Color("#B8504B"),
                fill_style=FillStyle.CROSS_HATCH,
            ),
            EcuClassificationName.DOMAIN_GATEWAY: StyleAttributes(
                shape=Shape.DIAG_ROUND_RECTANGLE, fill_color=Color("#AAD6E2"), dx=6
            ),
            EcuClassificationName.NON_DOMAIN_GATEWAY: StyleAttributes(
                shape=Shape.DIAG_ROUND_RECTANGLE, fill_color=Color("#D4CCDF"), dx=6
            ),
            EcuClassificationName.LIN_CONNECTED_ECU: StyleAttributes(
                rounded=True,
                fill_color=Color("#EFD3D1"),
            ),
            EcuClassificationName.ENTRY_POINT: StyleAttributes(
                rounded=True,
                stroke_color=Color("#FDB409"),
                stroke_width=4,
            ),
            EcuClassificationName.CRITICAL_ELEMENT: StyleAttributes(
                rounded=True,
                stroke_color=Color("#FC0008"),
                stroke_width=4,
            ),
        },
        network_protocol_type_style_attributes={
            ProtocolTypeName.CAN: StyleAttributes(
                stroke_width=4,
                start_arrow=Arrow.NONE,
                end_arrow=Arrow.NONE,
                start_fill=False,
                end_fill=False,
                jump_style=JumpStyle.ARC,
            ),
            ProtocolTypeName.CAN_250: StyleAttributes(
                stroke_color=Color("#1A4654"),
                stroke_width=4,
                start_arrow=Arrow.NONE,
                end_arrow=Arrow.NONE,
                start_fill=False,
                end_fill=False,
                jump_style=JumpStyle.ARC,
            ),
            ProtocolTypeName.CAN_500: StyleAttributes(
                stroke_color=Color("#28728A"),
                stroke_width=4,
                start_arrow=Arrow.NONE,
                end_arrow=Arrow.NONE,
                start_fill=False,
                end_fill=False,
                jump_style=JumpStyle.ARC,
            ),
            ProtocolTypeName.CAN_800: StyleAttributes(
                stroke_color=Color("#82C2D3"),
                stroke_width=4,
                start_arrow=Arrow.NONE,
                end_arrow=Arrow.NONE,
                start_fill=False,
                end_fill=False,
                jump_style=JumpStyle.ARC,
            ),
            ProtocolTypeName.CAN_FD: StyleAttributes(
                stroke_color=Color("#B00005"),
                stroke_width=4,
                start_arrow=Arrow.NONE,
                end_arrow=Arrow.NONE,
                start_fill=False,
                end_fill=False,
                jump_style=JumpStyle.ARC,
            ),
            ProtocolTypeName.FLEX_RAY: StyleAttributes(
                stroke_color=Color("#FEBDFF"),
                stroke_width=4,
                start_arrow=Arrow.NONE,
                end_arrow=Arrow.NONE,
                start_fill=False,
                end_fill=False,
                jump_style=JumpStyle.ARC,
            ),
            ProtocolTypeName.ETHERNET: StyleAttributes(
                stroke_color=Color("#C1B4D0"),
                stroke_width=4,
                start_arrow=Arrow.NONE,
                end_arrow=Arrow.NONE,
                start_fill=False,
                end_fill=False,
                jump_style=JumpStyle.ARC,
            ),
            ProtocolTypeName.MOST_ELECTRIC: StyleAttributes(
                stroke_color=Color("#F18B45"),
                stroke_width=4,
                start_arrow=Arrow.NONE,
                end_arrow=Arrow.NONE,
                start_fill=False,
                end_fill=False,
                jump_style=JumpStyle.ARC,
            ),
            ProtocolTypeName.LIN: StyleAttributes(
                stroke_color=Color("#81CA3F"),
                stroke_width=4,
                start_arrow=Arrow.NONE,
                end_arrow=Arrow.NONE,
                start_fill=False,
                end_fill=False,
                jump_style=JumpStyle.ARC,
            ),
        },
    )

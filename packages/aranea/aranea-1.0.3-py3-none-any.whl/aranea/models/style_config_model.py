"""
This module provides a pydantic model for working with style configurations.
"""

from enum import Enum
from typing import Literal, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.color import Color

from aranea.models.custom_xml_shapes.split_border_rectangle import (
    CornerStyle, SplitBorderRectangleFactory)
from aranea.models.graph_model import (EcuClassification,
                                       EcuClassificationName,
                                       NetworkDFFClassification, NodeType,
                                       ProtocolType, ProtocolTypeName)
from aranea.models.style_config_model_utils import merge_models
from aranea.models.xml_model import (MxCellStyle, MxCellStyleAlign,
                                     MxCellStyleArrow, MxCellStyleDefaultShape,
                                     MxCellStyleFillStyle,
                                     MxCellStyleJumpStyle,
                                     MxCellStylePerimeter, MxCellStyleShape,
                                     MxCellStyleVerticalAlign,
                                     MxCellWhiteSpace)

DEFAULT_DASH_PATTERN_FACTOR_DASHED = 8 / 12  # default rem_size = 12, default stroke/spacing = 8
DEFAULT_DASH_PATTERN_FACTOR_DOTTED_SPACING = (
    4 / 12
)  # default rem_size = 12, default spacing size = 4
DEFAULT_DASH_PATTERN_FACTOR_DOTTED_DOT = 1 / 12  # default rem_size = 12, default stroke = 1


class FillStyle(Enum):
    """
    Enum for defining the fill style.
    """

    SOLID = "SOLID"
    HATCH = "HATCH"
    CROSS_HATCH = "CROSS_HATCH"


class Shape(Enum):
    """
    Enum for defining the shape.
    """

    RECTANGLE = "RECTANGLE"
    ELLIPSE = "ELLIPSE"
    TEXT = "TEXT"
    WAYPOINT = "WAYPOINT"
    DIAG_ROUND_RECTANGLE = "DIAG_ROUND_RECTANGLE"
    IMAGE = "IMAGE"


class TextDirection(Enum):
    """
    Enum for defining the text direction.
    """

    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"


class Align(Enum):
    """
    Enum for defining the text alignment.
    """

    CENTER = "CENTER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class VerticalAlign(Enum):
    """
    Enum for defining the vertical text alignment.
    """

    MIDDLE = "MIDDLE"
    TOP = "TOP"
    BOTTOM = "BOTTOM"


class Perimeter(Enum):
    """
    Enum for defining the perimeter.
    """

    CENTER = "CENTER"


class WhiteSpace(Enum):
    """
    Enum for defining how to deal with white space.
    """

    WRAP = "WRAP"


class Arrow(Enum):
    """
    Enum for defining the arrow style.
    """

    CLASSIC = "CLASSIC"
    NONE = "NONE"


class JumpStyle(Enum):
    """
    Enum for defining the jump style.
    """

    NONE = "NONE"
    ARC = "ARC"
    GAP = "GAP"
    SHARP = "SHARP"
    LINE = "LINE"


ColorDescriptor = Color | Literal["NONE"] | None


class StyleAttributes(BaseModel):
    """
    Model for defining style attributes.
    """

    model_config = ConfigDict(extra="forbid")

    shape: Shape | None = Field(
        default=None,
    )
    rounded: bool | None = Field(
        default=None, description="Mainly used in combination with Shape.RECTANGLE"
    )
    fill_color: ColorDescriptor = Field(
        default=None,
    )
    fill_style: FillStyle | None = Field(
        default=None,
    )
    stroke_color: ColorDescriptor = Field(
        default=None,
    )
    stroke_width: int | None = Field(
        default=None,
    )
    text_direction: TextDirection | None = Field(
        default=None,
    )
    resizable: bool | None = Field(
        default=None,
    )
    rotatable: bool | None = Field(
        default=None,
    )
    autosize: bool | None = Field(
        default=None,
    )
    align: Align | None = Field(
        default=None,
    )
    vertical_align: VerticalAlign | None = Field(
        default=None,
    )
    size: int | None = Field(
        default=None,
    )
    perimeter: Perimeter | None = Field(
        default=None, description="Mainly used in combination with Shape.WAYPOINT"
    )
    white_space: WhiteSpace | None = Field(
        default=None,
    )
    start_arrow: Arrow | None = Field(
        default=None,
    )
    start_fill: bool | None = Field(
        default=None,
    )
    end_arrow: Arrow | None = Field(
        default=None,
    )
    end_fill: bool | None = Field(
        default=None,
    )
    dx: float | None = Field(
        default=None,
    )
    dashed: bool | None = Field(
        default=None,
    )
    dash_pattern: str | None = Field(
        default=None,
    )
    jump_style: JumpStyle | None = Field(
        default=None,
    )


def map_color_descriptor(style_attributes_color_descriptor: ColorDescriptor) -> str | None:
    """
    Function for mapping a color descriptor to its corresponding XML attribute value.

    :param style_attributes_color_descriptor: ColorDescriptor to be mapped
    :type style_attributes_color_descriptor: ColorDescriptor
    :return: Optional hex color string
    :rtype: str | None
    """
    if style_attributes_color_descriptor:
        if isinstance(style_attributes_color_descriptor, Color):
            return style_attributes_color_descriptor.as_hex(format="long")
        if style_attributes_color_descriptor == "NONE":
            return "none"
    return None


def map_shape(
    style_attributes: StyleAttributes, stroke_colors: list[str]
) -> MxCellStyleShape | None:
    """
    Function for mapping style attributes and stroke
    colors to the corresponding XML attribute value.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :param stroke_colors: Stroke colors to be mapped
    :type stroke_colors: list[str]
    :return: Corresponding MxCellStyleShape value
    :rtype: MxCellStyleShape
    """
    stroke_colors_len = len(stroke_colors)

    if stroke_colors_len > 2:
        raise ValueError("Currently only shapes with up to two stroke colors are supported.")

    if stroke_colors_len == 2:
        factory = SplitBorderRectangleFactory()
        match style_attributes.shape:
            case Shape.DIAG_ROUND_RECTANGLE:
                return factory.get_split_border_rectangle_shape(
                    stroke_colors[0], stroke_colors[1], CornerStyle.DIAG_ROUND
                )
            case Shape.RECTANGLE:
                return factory.get_split_border_rectangle_shape(
                    stroke_colors[0], stroke_colors[1], CornerStyle.ROUND
                )
            case _:
                raise ValueError("The used shape does not support more than one stroke color.")

    # only one stroke color
    match style_attributes.shape:
        case Shape.RECTANGLE:
            return MxCellStyleDefaultShape.RECTANGLE
        case Shape.ELLIPSE:
            return MxCellStyleDefaultShape.ELLIPSE
        case Shape.TEXT:
            return MxCellStyleDefaultShape.TEXT
        case Shape.WAYPOINT:
            return MxCellStyleDefaultShape.WAYPOINT
        case Shape.DIAG_ROUND_RECTANGLE:
            return MxCellStyleDefaultShape.DIAG_ROUND_RECTANGLE
        case Shape.IMAGE:
            return MxCellStyleDefaultShape.IMAGE
        case _:
            return None  # for edges


def map_rounded(style_attributes: StyleAttributes) -> Optional[bool]:
    """
    Function for mapping the StyleAttributes' `rounded` value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[bool]
    """
    return style_attributes.rounded


def map_fill_color(style_attributes: StyleAttributes) -> Optional[str]:
    """
    Function for mapping the StyleAttributes' `fill_color`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[str]
    """
    return map_color_descriptor(style_attributes.fill_color)


def map_fill_style(style_attributes: StyleAttributes) -> Optional[MxCellStyleFillStyle]:
    """
    Function for mapping the StyleAttributes' `fill_style`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[MxCellStyleFillStyle]
    """
    match style_attributes.fill_style:
        case FillStyle.SOLID:
            return MxCellStyleFillStyle.SOLID
        case FillStyle.HATCH:
            return MxCellStyleFillStyle.HATCH
        case FillStyle.CROSS_HATCH:
            return MxCellStyleFillStyle.CROSS_HATCH
        case _:
            return None


def map_stroke_color(style_attributes: StyleAttributes) -> Optional[str]:
    """
    Function for mapping the StyleAttributes' `stroke_color`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[str]
    """
    return map_color_descriptor(style_attributes.stroke_color)


def map_stroke_width(style_attributes: StyleAttributes) -> Optional[int]:
    """
    Function for mapping the StyleAttributes' `stroke_width`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[int]
    """
    return style_attributes.stroke_width


def map_text_horizontal(style_attributes: StyleAttributes) -> Optional[bool]:
    """
    Function for mapping the StyleAttributes' `text_direction`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[bool]
    """
    match style_attributes.text_direction:
        case TextDirection.HORIZONTAL:
            return True
        case TextDirection.VERTICAL:
            return False
        case _:
            return None


def map_resizable(style_attributes: StyleAttributes) -> Optional[bool]:
    """
    Function for mapping the StyleAttributes' `resizable`
    value to the corresponding XML attributes.'

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[bool]
    """
    return style_attributes.resizable


def map_rotatable(style_attributes: StyleAttributes) -> Optional[bool]:
    """
    Function for mapping the StyleAttributes' `rotatable`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[bool]
    """
    return style_attributes.rotatable


def map_autosize(style_attributes: StyleAttributes) -> Optional[bool]:
    """
    Function for mapping the StyleAttributes' `autosize`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[bool]
    """
    return style_attributes.autosize


def map_align(style_attributes: StyleAttributes) -> Optional[MxCellStyleAlign]:
    """
    Function for mapping the StyleAttributes' `align`
    value to the corresponding XML attributes.'

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[MxCellStyleAlign]
    """
    match style_attributes.align:
        case Align.CENTER:
            return MxCellStyleAlign.CENTER
        case Align.LEFT:
            return MxCellStyleAlign.LEFT
        case Align.RIGHT:
            return MxCellStyleAlign.RIGHT
        case _:
            return None


def map_vertical_align(style_attributes: StyleAttributes) -> Optional[MxCellStyleVerticalAlign]:
    """
    Function for mapping the StyleAttributes' `vertical_align`
    value to the corresponding XML attributes.'

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[MxCellStyleVerticalAlign]
    """
    match style_attributes.vertical_align:
        case VerticalAlign.MIDDLE:
            return MxCellStyleVerticalAlign.MIDDLE
        case VerticalAlign.TOP:
            return MxCellStyleVerticalAlign.TOP
        case VerticalAlign.BOTTOM:
            return MxCellStyleVerticalAlign.BOTTOM
        case _:
            return None


def map_size(style_attributes: StyleAttributes) -> Optional[int]:
    """
    Function for mapping the StyleAttributes' `size`
    value to the corresponding XML attributes.'

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[int]
    """
    return style_attributes.size


def map_perimeter(style_attributes: StyleAttributes) -> Optional[MxCellStylePerimeter]:
    """
    Function for mapping the StyleAttributes' `perimeter`
    value to the corresponding XML attributes.'

    :param style_attributes: StyleAttributes to be mapped
    :param style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[MxCellStylePerimeter]
    """
    match style_attributes.perimeter:
        case Perimeter.CENTER:
            return MxCellStylePerimeter.CENTER_PERIMETER
        case _:
            return None


def map_white_space(style_attributes: StyleAttributes) -> Optional[MxCellWhiteSpace]:
    """
    Function for mapping the StyleAttributes' `white_space`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellWhiteSpace value
    :rtype: Optional[MxCellWhiteSpace]
    """
    match style_attributes.white_space:
        case WhiteSpace.WRAP:
            return MxCellWhiteSpace.WRAP
        case _:
            return None


def map_arrow(arrow_descriptor: Arrow | None) -> Optional[MxCellStyleArrow]:
    """
    Function for mapping the StyleAttributes' `start_arrow` or
    'end_arrow' value to the corresponding XML attribute.

    :param arrow_descriptor: Arrow descriptor to be mapped
    :type arrow_descriptor: Arrow
    :return: Corresponding MxCellStyleArrow value
    :rtype: Optional[MxCellStyleArrow]
    """
    match arrow_descriptor:
        case Arrow.CLASSIC:
            return MxCellStyleArrow.CLASSIC
        case Arrow.NONE:
            return MxCellStyleArrow.NONE
        case _:
            return None


def map_arrow_fill(arrow_fill: bool | None) -> Optional[bool]:
    """
    Function for mapping the StyleAttributes' `start_fill`
    or 'end_fill' value to the corresponding XML attribute.

    :param arrow_fill: Arrow fill to be mapped
    :type arrow_fill: bool
    :return: Corresponding MxCellStyle value
    :rtype: Optional[bool]
    """
    return arrow_fill


def map_dx(dx: float | None) -> Optional[float]:
    """
    Function for mapping the StyleAttributes' `dx`
    value to the corresponding XML attribute.

    :param dx: dx to be mapped
    :type dx: float
    :return: Corresponding MxCellStyle value
    :rtype: Optional[float]
    """
    return dx


def map_dashed(dashed: bool | None) -> Optional[bool]:
    """
    Function for mapping the StyleAttributes' `dashed`
    value to the corresponding XML attribute.

    :param dashed: dashed to be mapped
    :type dashed: bool
    :return: Corresponding MxCellStyle value
    :rtype: Optional[bool]
    """
    return dashed


def map_dash_pattern(dash_pattern: str | None) -> Optional[str]:
    """
    Function for mapping the StyleAttributes' `dash_pattern`
    value to the corresponding XML attribute.

    :param dash_pattern: dash_pattern to be mapped
    :type dash_pattern: str
    :return: Corresponding MxCellStyle value
    :rtype: Optional[str]
    """
    return dash_pattern


def map_jump_style(jump_style: JumpStyle | None) -> Optional[MxCellStyleJumpStyle]:
    """
    Function for mapping the StyleAttributes' `jump_style`
    value to the corresponding XML attribute.

    :param jump_style: jump_style to be mapped
    :type jump_style: str
    :return: Corresponding MxCellStyle value
    :rtype: Optional[str]
    """
    match jump_style:
        case JumpStyle.NONE:
            return MxCellStyleJumpStyle.NONE
        case JumpStyle.ARC:
            return MxCellStyleJumpStyle.ARC
        case JumpStyle.GAP:
            return MxCellStyleJumpStyle.GAP
        case JumpStyle.SHARP:
            return MxCellStyleJumpStyle.SHARP
        case JumpStyle.LINE:
            return MxCellStyleJumpStyle.LINE
        case _:
            return None


class StyleConfig(BaseModel):
    """
    Model for defining a style config.
    """

    model_config = ConfigDict(
        extra="forbid",
        title="Style Config Schema",
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "id": "https://gitlab.uni-ulm.de/se/mbti/automated-architecture-analysis"
            + "/src/aranea/models/style-config-schema-v1.0.json",
        },
    )

    rem_size: float = 12.0
    node_type_style_attributes: dict[NodeType, StyleAttributes] | None = None
    node_classification_style_attributes: dict[EcuClassificationName, StyleAttributes] | None = None
    network_protocol_type_style_attributes: dict[ProtocolTypeName, StyleAttributes] | None = None

    def get_node_type_style_attributes(self, node_type: NodeType) -> StyleAttributes | None:
        """
        Function for getting the style attributes for a node type.

        :param node_type: NodeType to get the style attributes for
        :type node_type: NodeType
        :return Corresponding style attributes
        :rtype: StyleAttributes | None
        """
        if self.node_type_style_attributes is None:
            return None

        return self.node_type_style_attributes.get(node_type)

    def get_network_protocol_style_attributes(
        self, protocol: ProtocolType
    ) -> StyleAttributes | None:
        """
        Function for getting the style attributes for a network protocol.

        :param protocol: ProtocolType to get the style attributes for
        :type protocol: ProtocolType
        :return: Corresponding style attributes
        :rtype: StyleAttributes | None
        """

        if self.network_protocol_type_style_attributes is None:
            return None

        return self.network_protocol_type_style_attributes.get(protocol.name)

    def get_node_classifications_style_attributes(
        self, node_classifications: list[EcuClassification]
    ) -> list[StyleAttributes] | None:
        """
        Function for getting the style attributes for a node classifications.

        :param node_classifications: Node classifications to get the style attributes for
        :type node_classifications: list[EcuClassification]

        :return: Corresponding style attributes list
        :rtype: list[StyleAttributes] | None
        """
        if not self.node_classification_style_attributes:
            return None

        classification_styles: list[StyleAttributes] = []

        for classification in node_classifications:
            if classification.name not in self.node_classification_style_attributes:
                continue

            classification_styles.append(
                self.node_classification_style_attributes[classification.name]
            )

        return classification_styles if len(classification_styles) > 0 else None

    def get_combined_style_attributes_and_stroke_colors(
        self,
        *,
        node_type: Optional[NodeType] = None,
        node_classifications: Optional[list[EcuClassification]] = None,
        protocol_type: Optional[ProtocolType] = None,
        network_dff_classification: Optional[NetworkDFFClassification] = None,
    ) -> Tuple[StyleAttributes, list[str]]:
        """
        Function for combining style attributes based on NodeType,
        EcuClassifications and ProtocolType.

        :param node_type: NodeType to get the style attributes for
        :type node_type: NodeType
        :param node_classifications: EcuClassifications to get the style attributes for
        :type node_classifications: list[EcuClassification]
        :param protocol_type: ProtocolType to get the style attributes for
        :type protocol_type: ProtocolType

        :return: Corresponding style attributes and color list
        :rtype: Tuple[StyleAttributes, list[str]]
        """
        stroke_colors: list[str] = []  # keep track if multiple stroke colors should apply
        style_attributes: StyleAttributes = StyleAttributes()

        if node_type:
            if node_type_style_attributes := self.get_node_type_style_attributes(node_type):
                style_attributes = merge_models(
                    style_attributes, node_type_style_attributes, StyleAttributes
                )
                if node_type_stroke_colors := map_color_descriptor(
                    node_type_style_attributes.stroke_color
                ):
                    stroke_colors.append(node_type_stroke_colors)

        if node_classifications:
            if node_classifications_styles_attributes := (
                self.get_node_classifications_style_attributes(node_classifications)
            ):
                cleared_stroke_colors = False  # this is needed because node_type stroke colors
                # should be overwritten by node_classification stroke colors
                for (
                    classification_style_attributes
                ) in node_classifications_styles_attributes:  # pylint: disable=not-an-iterable
                    if classification_stroke_color := map_color_descriptor(
                        classification_style_attributes.stroke_color
                    ):
                        if not cleared_stroke_colors:
                            stroke_colors.clear()
                            cleared_stroke_colors = True
                        stroke_colors.append(classification_stroke_color)
                    style_attributes = merge_models(
                        style_attributes, classification_style_attributes, StyleAttributes
                    )

        if network_dff_classification:
            style_attributes.dashed = True
            if network_dff_classification == NetworkDFFClassification.NEW_NW:
                style_attributes.dash_pattern = (
                    str(self.rem_size * DEFAULT_DASH_PATTERN_FACTOR_DASHED)
                    + " "
                    + str(self.rem_size * DEFAULT_DASH_PATTERN_FACTOR_DASHED)
                )
            if network_dff_classification == NetworkDFFClassification.NW_ONLY_IN_BR:
                style_attributes.dash_pattern = (
                    str(self.rem_size * DEFAULT_DASH_PATTERN_FACTOR_DOTTED_DOT)
                    + " "
                    + str(self.rem_size * DEFAULT_DASH_PATTERN_FACTOR_DOTTED_SPACING)
                )

        if protocol_type:
            if protocol_type_styles_attributes := self.get_network_protocol_style_attributes(
                protocol_type
            ):
                style_attributes = merge_models(
                    style_attributes, protocol_type_styles_attributes, StyleAttributes
                )
                if protocol_type_stroke_colors := map_color_descriptor(
                    protocol_type_styles_attributes.stroke_color
                ):
                    stroke_colors.append(protocol_type_stroke_colors)

        return style_attributes, stroke_colors

    def get_mx_cell_style(
        self,
        *,
        node_type: Optional[NodeType] = None,
        node_classifications: Optional[list[EcuClassification]] = None,
        protocol_type: Optional[ProtocolType] = None,
        network_dff_classification: Optional[NetworkDFFClassification] = None,
    ) -> MxCellStyle:
        """
        Function for getting the `MxCellStyle` based on NodeType,
        EcuClassifications, NetworkDFFClassification and ProtocolType.

        :param node_type: NodeType to get the style attributes for
        :type node_type: NodeType
        :param node_classifications: EcuClassifications to get
            the style attributes for
        :type node_classifications: list[EcuClassification]
        :param protocol_type: ProtocolType to get the style attributes for
        :type protocol_type: ProtocolType
        :param network_dff_classification: NetworkDFFClassification to get the style attributes for
        :type network_dff_classification: NetworkDFFClassification

        :return: Composed cell style
        :rtype: MxCellStyle
        """
        combined_style_attributes, stroke_colors = (
            self.get_combined_style_attributes_and_stroke_colors(
                node_type=node_type,
                node_classifications=node_classifications,
                protocol_type=protocol_type,
                network_dff_classification=network_dff_classification,
            )
        )
        mx_cell_shape = map_shape(combined_style_attributes, stroke_colors)

        return MxCellStyle(
            shape=mx_cell_shape,
            rounded=map_rounded(combined_style_attributes),
            fillColor=map_fill_color(combined_style_attributes),
            fillStyle=map_fill_style(combined_style_attributes),
            strokeColor=map_stroke_color(combined_style_attributes),
            strokeWidth=map_stroke_width(combined_style_attributes),
            horizontal=map_text_horizontal(combined_style_attributes),
            resizable=map_resizable(combined_style_attributes),
            rotatable=map_rotatable(combined_style_attributes),
            autosize=map_autosize(combined_style_attributes),
            align=map_align(combined_style_attributes),
            verticalAlign=map_vertical_align(combined_style_attributes),
            size=map_size(combined_style_attributes),
            perimeter=map_perimeter(combined_style_attributes),
            whiteSpace=map_white_space(combined_style_attributes),
            startArrow=map_arrow(combined_style_attributes.start_arrow),
            startFill=map_arrow_fill(combined_style_attributes.start_fill),
            endArrow=map_arrow(combined_style_attributes.end_arrow),
            endFill=map_arrow_fill(combined_style_attributes.end_fill),
            dx=map_dx(combined_style_attributes.dx),
            dashed=map_dashed(combined_style_attributes.dashed),
            dashPattern=map_dash_pattern(combined_style_attributes.dash_pattern),
            jumpStyle=map_jump_style(combined_style_attributes.jump_style),
        )

"""
Module for generating the drawio custom shape: Split Boarder Rectangle
"""

from enum import Enum
from typing import Dict

from jinja2 import Template

from aranea.models.custom_xml_shapes import jinja_environment
from aranea.models.custom_xml_shapes.custom_xml_shapes_utils import (
    encode_xml_str, is_valid_hex_color)


class CornerStyle(Enum):
    """
    Enum class for the corner styles of a split border rectangle.
    """

    ROUND = "ROUND"
    SQUARE = "SQUARE"
    DIAG_ROUND = "DIAG_ROUND"


class SplitBorderRectangleFactory:
    """
    Class for creating a split border rectangle custom shape in drawio.
    """

    corner_style_template_names: Dict[CornerStyle, str] = {
        CornerStyle.ROUND: "split_border_rectangle_round_corners.xml.jinja",
        CornerStyle.SQUARE: "split_border_rectangle_square_corners.xml.jinja",
        CornerStyle.DIAG_ROUND: "split_border_rectangle_diag_round_corners.xml.jinja",
    }

    def get_split_border_rectangle_shape(
        self, color_1: str, color_2: str, corner_style: CornerStyle
    ) -> str:
        """
        Factory function for generating an encoded custom shape stencil.

        :param color_1: First color of the border (upper half) (hex color)
        :type color_1: str
        :param color_2: Second color of the border (lower half) (hex color)
        :type color_2: str
        :param corner_style: The style of the corners e.g. rounded
        :type corner_style: CornerStyle

        :return: The style encoded style string of the custom shape
        :rtype: str
        """
        if not is_valid_hex_color(color_1) or not is_valid_hex_color(color_2):
            raise ValueError("Expected a valid hex color argument string")

        shape_template: Template = jinja_environment.get_template(
            self.corner_style_template_names[corner_style]
        )
        shape_str: str = shape_template.render(color_1=color_1, color_2=color_2)

        encoded_xml_str: str = encode_xml_str(shape_str)
        shape: str = "stencil(" + encoded_xml_str + ")"
        return shape

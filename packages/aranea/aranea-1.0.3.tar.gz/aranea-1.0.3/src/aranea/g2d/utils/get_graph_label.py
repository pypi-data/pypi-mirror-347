"""
Module that provides a function for creating graph labels
"""

from aranea.g2d.utils.get_graph_boundaries import Boundaries
from aranea.models.graph_model import Text
from aranea.models.xml_model import (MxCellShape, MxCellStyle,
                                     MxCellStyleAlign, MxCellStyleDefaultShape,
                                     MxCellStyleVerticalAlign, MxGeometryShape)

DEFAULT_BOTTOM_MARGIN_FACTOR = 3
DEFAULT_DIMENSION_FACTOR = 3


def get_graph_label(label: Text, graph_boundaries: Boundaries, rem_size: float) -> MxCellShape:
    """
    Function for creating a graph label mx cell.

    :param graph_boundaries: Boundaries of the graph
    :type graph_boundaries: Boundaries
    :return: Graph label mx cell
    :rtype: MxCellShape
    """
    return MxCellShape(
        attr_value=label[0],
        geometry=MxGeometryShape(
            attr_x=(graph_boundaries[0][0] + graph_boundaries[1][0]) / 2
            - label[2] * rem_size * DEFAULT_DIMENSION_FACTOR / 2,
            attr_y=graph_boundaries[1][1] + label[2] * rem_size * DEFAULT_BOTTOM_MARGIN_FACTOR,
            attr_height=label[2] * rem_size * DEFAULT_DIMENSION_FACTOR,
            attr_width=label[2] * rem_size * DEFAULT_DIMENSION_FACTOR,
        ),
        attr_style=MxCellStyle(
            shape=MxCellStyleDefaultShape.TEXT,
            align=MxCellStyleAlign.CENTER,
            verticalAlign=MxCellStyleVerticalAlign.MIDDLE,
            fontSize=label[2] * rem_size,
            strokeColor="none",
            fillColor="none",
        ).to_semicolon_string(),
    )

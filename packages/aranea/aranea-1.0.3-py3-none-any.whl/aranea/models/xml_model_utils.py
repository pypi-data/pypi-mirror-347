"""
This module provides utility functions for working with the xml model.
"""

from typing import Sequence
from uuid import UUID, uuid4

from aranea.models.xml_model import MxCell, RootCells


def assign_parent_id(cell: RootCells, parent_id: UUID) -> RootCells:
    """
    Function for setting the parent id on cells accepted by the <root /> element.

    :param cell: The cell where the parent id shall be set.
    :type cell: RootCells
    :param parent_id: The UUID of the respective parent element
    :type parent_id: UUID
    :return:
    """
    cell.attr_parent = parent_id
    return cell


def get_xml_layer(
    cells: Sequence[RootCells],
    *,
    layer_uuid: UUID = uuid4(),
    root_uuid: UUID = uuid4(),
) -> list[RootCells]:
    """
    Function for generating a default layer structure with a single layer
    :param cells: The cells that shall be painted onto the generated layer.
    :type cells: Sequence[RootCells]
    :param layer_uuid: The UUID of the respective layer
    :type layer_uuid: UUID
    :param root_uuid: The UUID of the respective root element
    :type root_uuid: UUID
    :return:
    """
    root_cell = MxCell(attr_id=root_uuid)
    layer_cell = MxCell(
        attr_id=layer_uuid,
        attr_value="Layer 1",
        attr_parent=root_cell.attr_id,
    )

    return [
        root_cell,
        layer_cell,
        *list(map(lambda cell: assign_parent_id(cell, layer_cell.attr_id), cells)),
    ]

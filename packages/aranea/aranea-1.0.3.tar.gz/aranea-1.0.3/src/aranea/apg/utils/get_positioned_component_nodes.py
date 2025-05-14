"""
This module provides functions to get positioned component nodes
"""

import copy
from typing import Annotated
from uuid import UUID

from pydantic.types import UuidVersion

from aranea.apg.utils.attack_path_node_positioner import \
    AttackPathNodePositioner
from aranea.models.graph_model import ComponentNode, Network

# initial x, initial y, margin x, margin y
PositionalMargin = tuple[float, float, float, float]


def get_positioned_component_nodes(
    original_nodes: dict[Annotated[UUID, UuidVersion(4)], ComponentNode],
    networks: list[Network],
    start: UUID,
    end: UUID,
    positional_margin: PositionalMargin,
) -> dict[Annotated[UUID, UuidVersion(4)], ComponentNode]:
    """
    Function to get positioned component nodes

    :param nodes: The nodes to be positioned
    :type nodes: dict[Annotated[UUID, UuidVersion(4)], ComponentNode]
    :param networks: The networks of the nodes
    :type networks: list[Network]
    :param start: The start node
    :type start: UUID
    :param end: The end node
    :type end: UUID
    :param positional_margin: The positional margin
    :type positional_margin: PositionalMargin
    :return: The positioned component nodes
    :rtype: dict[Annotated[UUID, UuidVersion(4)], ComponentNode]
    """

    # to prevent call by reference issues
    nodes = copy.deepcopy(original_nodes)

    # These values may be part of the CLI input
    positioner = AttackPathNodePositioner(
        initial_x=positional_margin[0],
        initial_y=positional_margin[1],
        margin_size_x=positional_margin[2],
        margin_size_y=positional_margin[3],
    )

    prev_uuid = start
    running_uuid = start

    while running_uuid != end:
        position = positioner.get_position()
        nodes[running_uuid].xRemFactor = position[0]
        nodes[running_uuid].yRemFactor = position[1]

        used_reverse = False

        used_edge, _ = next(
            (edge, network)
            for network in networks
            for edge in network.edges
            if (
                (edge.sourceId == running_uuid and edge.targetId != prev_uuid)
                or (edge.targetId == running_uuid and edge.sourceId != prev_uuid)
            )
        )

        if used_edge.targetId == running_uuid:
            used_reverse = True

        prev_uuid = running_uuid
        running_uuid = used_edge.targetId if not used_reverse else used_edge.sourceId

    position = positioner.get_position()
    nodes[end].xRemFactor = position[0]
    nodes[end].yRemFactor = position[1]

    return nodes

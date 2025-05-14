"""
This module provides functions for composing attack path graphs.
"""

from typing import Annotated, cast
from uuid import UUID

from pydantic.types import UuidVersion

from aranea.apg.utils.get_positioned_component_nodes import (
    PositionalMargin, get_positioned_component_nodes)
from aranea.models.graph_model import (AttackPathGraph, ComponentNode, Network,
                                       NodeUnionType, TechnicalCapability,
                                       TextOrientation)


def compose_attack_path_graph(
    nodes: dict[Annotated[UUID, UuidVersion(4)], ComponentNode],
    networks: list[Network],
    start: UUID,
    end: UUID,
    entry_technical_capability: TechnicalCapability,
    positional_margin: PositionalMargin,
) -> AttackPathGraph:
    """
    Function that composes an attack path graph from nodes and networks.

    :param nodes: The nodes to use.
    :type nodes: dict[Annotated[UUID, UuidVersion(4)], ComponentNode]
    :param networks: The networks to use.
    :type networks: list[Network]
    :param start: The start node to use.
    :type start: UUID
    :param end: The end node to use.
    :type end: UUID
    :param entry_technical_capability: The technical capability to use.
    :type entry_technical_capability: TechnicalCapability
    :param positional_margin: The positional margin to use.
    :type positional_margin: PositionalMargin
    :return: The composed attack path graph.
    :rtype: AttackPathGraph
    """
    start_ecu = nodes[start]
    end_ecu = nodes[end]

    start_ecu_name = "Unnamed ECU"
    end_ecu_name = "Unnamed ECU"

    if start_ecu is not None and start_ecu.innerText:
        start_ecu_name: str = start_ecu.innerText[0]

    if end_ecu is not None and end_ecu.innerText:
        end_ecu_name: str = end_ecu.innerText[0]

    positioned_component_nodes = get_positioned_component_nodes(
        nodes, networks, start, end, positional_margin
    )

    for network in networks:
        for edge in network.edges:
            if edge.text:
                edge.text = (edge.text[0], TextOrientation.HORIZONTAL, edge.text[2])

    return AttackPathGraph(
        label=(
            f"AttackPathGraph\nfrom: {start_ecu_name}({start})\nto:\
    {end_ecu_name}({end})\nvia technical capability: {entry_technical_capability.name.value}",
            TextOrientation.HORIZONTAL,
            1,
        ),
        nodes=cast(dict[UUID, NodeUnionType], positioned_component_nodes),
        networks=networks,
        entry_technical_capability=entry_technical_capability,
        entry_ecu=start,
        target_ecu=end,
    )

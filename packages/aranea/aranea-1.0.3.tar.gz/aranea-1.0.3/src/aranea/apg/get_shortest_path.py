"""
This module provides function for getting the shortest path in a graph
between two nodes.
"""

from __future__ import annotations

import logging
from math import log
from typing import Annotated, Any, Callable, cast
from uuid import UUID

import networkx as nx
from networkx.algorithms.shortest_paths.weighted import \
    single_source_bellman_ford
from pydantic.types import UuidVersion

from aranea.apg.get_component_node_feasibility_rating import \
    get_component_node_feasibility_rating
from aranea.models.graph_model import (ComponentNode, Edge, Network,
                                       TechnicalCapabilityName, Text)

logger = logging.getLogger(__name__)


def custom_weight_factory(
    graph: nx.Graph[UUID],
    start: UUID,
    end: UUID,
    technical_capability: TechnicalCapabilityName,
) -> Callable[[UUID, UUID, Any], float]:
    """
    Provides a custom weight function for the shortest path between two nodes.

    :param graph: Graph to calculate the weight for.
    :type graph: nx.Graph[UUID]
    :param start: Start node to calculate the weight for.
    :type start: UUID
    :param end: End node to calculate the weight for.
    :type end: UUID
    :param technical_capability: Technical capability name to use.
    :type technical_capability: TechnicalCapabilityName
    :return: The function for calculating a weight.
    """
    # In order to avoid reimplementing the Bellman-Ford-Algorithm for finding the shortest path
    # based on multiplying vales within [0,1] we use the -log of these values. With that we
    # can utilize the existing algorithms summation approach and still find the shortest path
    # with respect to the attack feasibility rating along a path.

    def custom_weight(node_u: UUID, node_v: UUID, data: Any) -> float:
        weight = 0

        weight += -log(data["source"].protocol_type.feasibility_rating)
        weight += -log(get_component_node_feasibility_rating(graph.nodes[node_u]["source"]))

        if node_u == start:
            tcs = [
                tc
                for tc in graph.nodes[node_u]["source"].technical_capabilities
                if tc.name == technical_capability
            ]
            if len(tcs) != 1:
                raise ValueError("Should only find one technical capability")
            weight += -log(tcs[0].feasibility_rating)

        if node_v == end:
            weight += -log(get_component_node_feasibility_rating(graph.nodes[node_v]["source"]))

        return weight

    return custom_weight


def get_shortest_path(
    weighted_graph: nx.Graph[UUID],
    start: UUID,
    end: UUID,
    technical_capability: TechnicalCapabilityName,
) -> tuple[dict[Annotated[UUID, UuidVersion(4)], ComponentNode], list[Network]] | None:
    """
    Function for getting the shortest path between two nodes.
    The shortest path is the one with the highest cumulative attack feasibility
    of all paths connecting the start and end nodes.

    :param weighted_graph: Graph in which to calculate the path.
    :type weighted_graph: nx.Graph[UUID]
    :param start: The node to calculate the shortest path from.
    :type start: UUID
    :param end: The node to calculate the shortest path to.
    :type end: UUID
    :param technical_capability: Technical capability name to use.
    :type technical_capability: TechnicalCapabilityNames
    :return: The shortest path from start to end.
    :rtype: tuple[dict[Annotated[UUID, UuidVersion(4)], ComponentNode], list[Network]]
    """

    if start not in weighted_graph.nodes:
        raise ValueError(f'Start node "{str(start)}" not found in the graph')
    if end not in weighted_graph.nodes:
        raise ValueError(f'End node "{str(end)}" not found in the graph')

    try:
        _, node_uuids = cast(
            tuple[float, list[UUID]],
            single_source_bellman_ford(
                weighted_graph,
                start,
                end,
                custom_weight_factory(weighted_graph, start, end, technical_capability),
            ),
        )

        nodes = cast(
            dict[Annotated[UUID, UuidVersion(4)], ComponentNode],
            {node_uuid: weighted_graph.nodes[node_uuid]["source"] for node_uuid in node_uuids},
        )

        # these networks only contain a single edge that is used for walking the shortest path
        networks: list[Network] = []

        for u, v in list(zip(node_uuids, node_uuids[1:])):
            source_network: Network = weighted_graph[u][v][
                "source"
            ].copy()  # pyright: ignore[reportArgumentType, reportAssignmentType]
            source_text: Text | None = next(
                (edge.text for edge in source_network.edges if edge.text), None
            )
            source_network.edges = [
                Edge(
                    sourceId=u,
                    targetId=v,
                    text=source_text,
                )
            ]

            networks.append(source_network)

        return nodes, networks
    except nx.NetworkXNoPath:
        logger.warning(
            "No path found from %s to %s. Does the graph contain unconnected components?",
            str(start),
            str(end),
        )
        return None
    except nx.NodeNotFound:
        logger.warning("No path found from %s to %s", str(start), str(end))
        return None

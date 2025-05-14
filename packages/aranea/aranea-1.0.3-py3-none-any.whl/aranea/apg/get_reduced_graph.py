"""
This module provides a function for reducing multi graphs to simple graphs.
"""

from __future__ import annotations

from typing import cast
from uuid import UUID

import networkx as nx

from aranea.models.graph_model import Network


def get_reduced_graph(graph: nx.MultiGraph[UUID]) -> nx.Graph[UUID]:
    """
    Function to get a reduced graph from a multi graph. The most feasible edge
    between two nodes survives.

    :param graph: The multi graph to get a reduced graph from
    :type graph: nx.MultiGraph
    :return: The reduced graph
    :rtype: nx.Graph
    """
    weighted_graph: nx.Graph[UUID] = nx.Graph()
    weighted_graph.add_nodes_from(graph.nodes(data=True))

    for u, v, data in graph.edges(data=True):
        if data.get("source") is None:
            raise ValueError("Missing source annotation")

        weight = cast(Network, data.get("source")).protocol_type.feasibility_rating

        if weighted_graph.has_edge(u, v):
            if (
                cast(
                    Network, weighted_graph[u][v]["source"]  # pyright: ignore [reportArgumentType]
                ).protocol_type.feasibility_rating
                < weight
            ):
                weighted_graph[u][v]["source"] = data.get(  # pyright: ignore [reportArgumentType]
                    "source"
                )
        else:
            weighted_graph.add_edge(u, v, source=data.get("source"))

    return weighted_graph

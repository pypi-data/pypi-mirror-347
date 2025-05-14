"""
This module provides function for creating networkx graphs.
"""

from __future__ import annotations

from uuid import UUID

import networkx as nx

from aranea.models.graph_model import Graph, NodeType, NodeUnionType


def is_component_node(node: NodeUnionType) -> bool:
    """
    Function to check if a node is a component node.
    :param node: The node to check.
    :type node: NodeUnionType
    :return: True if the node is a component node, False otherwise.
    :rtype: bool
    """
    return node.type == NodeType.COMPONENT


def get_networkx_graph(graph: Graph) -> nx.MultiGraph[UUID]:
    """
    Function to get a networkx graph from a graph.

    :param graph: The graph to get a networkx graph from.
    :type graph: Graph
    :return: A networkx multi graph.
    :rtype: nx.MultiGraph[UUID]
    """
    merged_graph: nx.MultiGraph[UUID] = (
        nx.MultiGraph()
    )  # There may be multiple networks between two ECUs.

    for node_id in graph.nodes:
        if not is_component_node(graph.nodes[node_id]):
            # We currently only work with ECUs that are directly connected to a network.
            # A reference in a network (represented by a TextNode) is therefore ignored.
            continue

        merged_graph.add_node(node_id, source=graph.nodes[node_id])

    for network in graph.networks:
        component_nodes: set[UUID] = set()

        for edge in network.edges:
            if is_component_node(graph.nodes[edge.sourceId]):
                component_nodes.add(edge.sourceId)

            if is_component_node(graph.nodes[edge.targetId]):
                component_nodes.add(edge.targetId)

        # Each network represents a complete graph.
        network_graph: nx.MultiGraph[UUID] = nx.complete_graph(component_nodes)

        # Add the edges of the complete network graph to the merged graph
        for u, v in network_graph.edges():
            merged_graph.add_edge(u, v, source=network)

    return merged_graph

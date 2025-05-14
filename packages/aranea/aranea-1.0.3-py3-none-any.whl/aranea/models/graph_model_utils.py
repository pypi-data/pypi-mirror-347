"""
Utility functions for the graph model module.
"""

from aranea.models.graph_model import AttackPathGraph, Graph


def is_attack_path_graph(graph: Graph | AttackPathGraph) -> bool:
    """
    Function for checking if handling a Graph or AttackPathGraph
    :param graph: Graph to check
    :type graph: Graph | AttackPathGraph
    :return: Boolean
    :rtype: bool
    """
    return bool(hasattr(graph, "entry_technical_capability"))

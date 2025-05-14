"""
This module provides a function that returns the feasibility rating of a component node.
"""

from functools import reduce

from aranea.models.graph_model import ComponentNode


def get_component_node_feasibility_rating(node: ComponentNode) -> float:
    """
    Function that returns the feasibility rating of a component node.

    :param node: The component node to get the feasibility rating for.
    :type node: ComponentNode
    :return: The feasibility rating of the component node.
    :rtype: float
    """
    default_feasibility = 1.0

    if len(node.classifications) == 0:
        return default_feasibility

    # TODO: is this really the right way to calculate a node feasibility rating?
    return reduce(
        lambda accumulated_feasibility, classification_y: accumulated_feasibility
        * classification_y.feasibility_rating,
        node.classifications,
        default_feasibility,
    )

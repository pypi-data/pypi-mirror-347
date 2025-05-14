"""
Module that provides a function for calculating the diagram page size
"""

from typing import Tuple

from aranea.g2d.utils.get_graph_boundaries import Boundaries
from aranea.models.style_config_model import StyleConfig


def get_graph_model_page_size(
    boundaries: Boundaries, style_config: StyleConfig, *, padding_factor: float = 8
) -> Tuple[float, float]:
    """
    Function that returns the diagram page size based on the component boundaries.

    :param boundaries: Boundaries of the contained components.
    :type boundaries: Boundaries
    :param style_config: StyleConfig of the diagram.
    :type style_config: StyleConfig
    :param padding_factor: Factor by which the padding is added.
    :type padding_factor: float
    :return: Tuple with page width and page height.
    :rtype: Tuple[float, float]
    """
    padding: float = style_config.rem_size * padding_factor

    return boundaries[1][0] + padding, boundaries[1][1] + padding

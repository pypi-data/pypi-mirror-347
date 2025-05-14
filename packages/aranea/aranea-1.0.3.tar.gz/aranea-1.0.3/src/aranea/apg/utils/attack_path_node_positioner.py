"""
This module provides a positioner for nodes
"""

from typing import Tuple


class AttackPathNodePositioner:
    """
    A class to provide a positioner for nodes
    """

    initial_x: float
    initial_y: float
    current_x: float
    current_y: float
    margin_size_x: float
    margin_size_y: float

    def __init__(
        self, initial_x: float, initial_y: float, margin_size_x: float, margin_size_y: float
    ) -> None:
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.margin_size_x = margin_size_x
        self.margin_size_y = margin_size_y

        self.current_x = self.initial_x
        self.current_y = self.initial_y

    def reset(self) -> None:
        """
        Reset the positioner
        :rtype: None
        """
        self.current_x = self.initial_x
        self.current_y = self.initial_y

    def get_position(self) -> Tuple[float, float]:
        """
        Returns the next position
        :return: The next position
        :rtype: Tuple[float, float]
        """
        position = self.current_x, self.current_y

        self.current_x += self.margin_size_x
        self.current_y += self.margin_size_y

        return position

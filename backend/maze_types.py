"""
This file is responsible for modules which are useful
during creating an algorithm for a maze output.
"""
from dataclasses import dataclass
from enum import Enum


@dataclass
class Cell:
    """
    walls: <do this later>
    visited: determies if the cell was visisted or not

    """
    walls: int = 15
    visited: bool = False


class Direction(Enum):
    """
    x determines an axis
    1 or -1 determines a direction
    1, 2, 4, 8 determines a wall

    """
    NORTH = "y 1 1"
    EAST = "x 1 2"
    SOUTH = "y -1 4"
    WEST = "x -1 8"

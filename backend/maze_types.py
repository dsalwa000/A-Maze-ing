"""
This file is responsible for modules which are useful
during creating an algorithm for a maze output.
"""
from dataclasses import dataclass
from enum import Enum


@dataclass
class Cell:
    """
    number: it is for counting cells
    walls: <do this later>
    visited: determies if the cell was visisted or not

    """
    number: int
    walls: int = 15
    visited: bool = False


class Direction(Enum):
    NORTH = "y 1 1"
    EAST = "x 1 2"
    SOUTH = "y -1 4"
    WEST = "x -1 8"

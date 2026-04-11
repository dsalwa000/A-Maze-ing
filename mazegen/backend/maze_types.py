"""
This file is responsible for modules which are useful
during creating an algorithm for a maze output.
"""
from dataclasses import dataclass
from enum import Enum


@dataclass
class Cell:
    """
    Single maze cell

    The maze uses a 4-bit bitmask to represent which
    are present around the cell (1 means the wall exists)

    Bit layout (binary -> direction):
        0001 (1): North
        0010 (2): East
        0100 (4): South
        1000 (8): West

    Examples:
        * walls == 1111 (15) means the cell is fully enclosed
        * walls == 0110 (6) means walls on the East and South sides

    Attributes:
        walls: Wall bitmask (default: 15)
        visited: Whether the generation algorithm has visited the cell
    """

    walls: int = 15
    visited: bool = False


class Direction(Enum):
    """
    x / y determines an axis
    1 / -1 determines a direction
    1, 2, 4, 8 determines a bitmask wall to destroy

    Examples:
        * "y 1 1" means y axis goes 1 ahead and it destroys North wall (1)
        * "x -1 8" means y axis goes -1 backwards and it destroys West wall (8)
    """
    NORTH = "y 1 1"
    EAST = "x 1 2"
    SOUTH = "y -1 4"
    WEST = "x -1 8"

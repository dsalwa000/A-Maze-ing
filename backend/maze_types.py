"""
This file is responsible for modules which are useful
during creating an algorithm for a maze output.
"""
from dataclasses import dataclass
from enum import Enum


@dataclass
class Cell:
    number: int
    walls: int = 15
    visited: bool = False
    forty_two: bool = True


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

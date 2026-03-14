"""
This file contains utils functions which are useful
during our converting process

"""
from maze_types import Cell, Direction
import random


def random_direction(
        cells: list[list[Cell]],
        max_x: int,
        max_y: int,
        x: int,
        y: int
) -> Direction:

    directions: list[Direction] = []

    if x > 0:
        if cells[x - 1][y].visited is False:
            directions.append(Direction.WEST)

    if y > 0:
        if cells[x][y - 1].visited is False:
            directions.append(Direction.SOUTH)

    if max_x - 1 > x:
        if cells[x + 1][y].visited is False:
            directions.append(Direction.EAST)

    if max_y - 1 > y:
        if cells[x][y + 1].visited is False:
            directions.append(Direction.NORTH)

    print(directions)

    return random.choice(directions)

"""
This file contains utils functions which are useful
during our converting process

"""
from maze_types import Cell, Direction
import random


def pick_direction(
        cells: list[list[Cell]],
        max_x: int,
        max_y: int,
        x: int,
        y: int
) -> list[str]:
    """
    This function finds nearby "not visited" positions and picks
    one of avaiable option

    """

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

    return random.choice(directions).value.split()


def change_position(direction: str, go_or_back: int, x: int, y: int) -> None:

    if direction == "x":
        x += int(go_or_back)
    else:
        y += int(go_or_back)


def remove_wall_at_cell(cell: Cell, wall: int) -> None:

    if wall == 0:
        cell.walls -= 2
    elif wall == 1:
        cell.walls -= 3
    elif wall == 2:
        cell.walls -= 0
    elif wall == 3:
        cell.walls -= 1

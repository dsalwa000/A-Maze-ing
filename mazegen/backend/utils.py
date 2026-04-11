"""
This file contains utils functions which are useful
during our converting process

"""
from mazegen.backend.maze_types import Cell, Direction
import random
from typing import Optional


def generate_maze(width: int, height: int) -> list[list[Cell]]:
    return [
        [Cell() for _ in range(height)] for _ in range(width)
    ]


def generate_42(
    width: int,
    height: int,
    maze: list[list[Cell]]
) -> int:
    """
    This function create a 42 sign at the center of a maze

    Returns:
    It returns amount of cells (int) which will be used as cells creating
    42 sign
    """
    x = 2 + (width - 10) // 2
    y = 7 + (height - 10) // 2
    count_42 = 0

    # Generate 4
    maze[x][y].visited = True
    count_42 += 1

    for _ in range(2):
        y -= 1
        maze[x][y].visited = True
        count_42 += 1

    for _ in range(2):
        x += 1
        maze[x][y].visited = True
        count_42 += 1

    for _ in range(2):
        y -= 1
        maze[x][y].visited = True
        count_42 += 1

    x = 6 + (width - 10) // 2
    y = 7 + (height - 10) // 2

    # Generate 2
    maze[x][y].visited = True
    count_42 += 1

    for _ in range(2):
        x += 1
        maze[x][y].visited = True
        count_42 += 1

    for _ in range(2):
        y -= 1
        maze[x][y].visited = True
        count_42 += 1

    for _ in range(2):
        x -= 1
        maze[x][y].visited = True
        count_42 += 1

    for _ in range(2):
        y -= 1
        maze[x][y].visited = True
        count_42 += 1

    for _ in range(2):
        x += 1
        maze[x][y].visited = True
        count_42 += 1

    return count_42


def avaiable_directions(
    maze: list[list[Cell]],
    max_x: int,
    max_y: int,
    x: int,
    y: int
) -> list[Direction]:
    """
    This function shows returns avaiable direction for a specyfic position

    """
    directions: list[Direction] = []

    if x > 0:
        if maze[x - 1][y].visited is False:
            directions.append(Direction.WEST)

    if y > 0:
        if maze[x][y - 1].visited is False:
            directions.append(Direction.SOUTH)

    if max_x - 1 > x:
        if maze[x + 1][y].visited is False:
            directions.append(Direction.EAST)

    if max_y - 1 > y:
        if maze[x][y + 1].visited is False:
            directions.append(Direction.NORTH)

    return directions


def pick_direction(
    directions: list[Direction],
) -> Optional[tuple[list[str], bool]] | None:
    """
    Pick randomly a nearby not-visited direction

    Returns (parts, to_save) where
        parts: is a 3-item list of strings [axis, step, wall]
        (look at the Direction Enum)
        to_save: returns True when the cell had more than option to go
    """

    if not directions:
        return None

    to_save = len(directions) > 1
    return random.choice(directions).value.split(), to_save


def change_position(
    direction: str,
    go_or_back: int,
    x: int,
    y: int,
) -> tuple[int, int]:

    if direction == "x":
        x += go_or_back
    elif direction == "y":
        y += go_or_back

    return x, y


def remove_wall_at_next_cell(cell: Cell, wall: int) -> None:

    if wall == 1:
        cell.walls -= 4
    elif wall == 2:
        cell.walls -= 8
    elif wall == 4:
        cell.walls -= 1
    elif wall == 8:
        cell.walls -= 2


def create_final_string(
    maze: list[list[Cell]],
    height: int,
    width: int
) -> list[str]:
    maze_str = []

    for j in range(height - 1, -1, -1):
        line = []

        for i in range(0, width):
            line.append(format(maze[i][j].walls & 0xF, "x"))

        maze_str.append("".join(line))

    return maze_str


def go_to_next_cell(
    maze: list[list[Cell]],
    picked_wall: int,
    x: int,
    y: int
) -> Cell:
    """
    The function goes to a next cell and returns it

    """
    next_cell: Cell = None

    if picked_wall == 1:
        next_cell = maze[x][y + 1]
    elif picked_wall == 2:
        next_cell = maze[x + 1][y]
    elif picked_wall == 4:
        next_cell = maze[x][y - 1]
    elif picked_wall == 8:
        next_cell = maze[x - 1][y]

    return next_cell


def make_maze_imperfect(
    maze: list[list[Cell]],
    height: int,
    width: int
) -> None:
    """
    This function randomly destroys walls inside a maze
    to makes it imperfect

    Each iteration alters one cell inside single 3x3 square
    inside the maze

    """
    start_y: int = height - 1
    end_y: int = height - 3

    while end_y >= 0:
        start_x: int = 0
        end_x: int = 2

        while end_x < width:
            x = random.randint(start_x, end_x)
            y = random.randint(end_y, start_y)

            # It secures the 42 sign
            if maze[x][y].walls == 15:
                start_x += 3
                end_x += 3
                continue

            """
            directions indexes:
            0 - North, 1 - East, 2 - South, 3 - West

            """
            directions: list[int] = [
                maze[x][y].walls & mask for mask in (1, 2, 4, 8)
            ]
            directions_cpy: list[int] = directions.copy()

            if (x == 0 or directions_cpy[3] == 0
                    or maze[x - 1][y].walls == 15):
                directions.remove(directions_cpy[3])

            if (x == width - 1 or directions_cpy[1] == 0
                    or maze[x + 1][y].walls == 15):
                directions.remove(directions_cpy[1])

            if (y == height - 1 or directions_cpy[0] == 0
                    or maze[x][y + 1].walls == 15):
                directions.remove(directions_cpy[0])

            if (y == 0 or directions_cpy[2] == 0
                    or maze[x][y - 1].walls == 15):
                directions.remove(directions_cpy[2])

            if not directions:
                continue

            picked_wall: Cell = random.choice(directions)
            maze[x][y].walls -= picked_wall

            next_cell = go_to_next_cell(maze, picked_wall, x, y)
            remove_wall_at_next_cell(next_cell, picked_wall)

            start_x += 3
            end_x += 3

        start_y -= 3
        end_y -= 3

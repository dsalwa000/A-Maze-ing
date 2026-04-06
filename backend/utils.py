"""
This file contains utils functions which are useful
during our converting process

"""
from maze_types import Cell, Direction
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
    This function create a 42 sign at the center of a maze.

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
) -> Optional[tuple[list[str], bool]]:
    """Pick randomly a nearby not-visited direction.

    Returns (parts, to_save) where parts is a 3-item list of strings
    [axis, step, wall] and to_save indicates whether the current position
    should be saved for backtracking. Returns None if there are no options.
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


def create_and_display_maze(
    maze: list[list[Cell]],
    height: int,
    width: int
) -> list[str]:
    maze_str = []

    for j in range(height - 1, -1, -1):
        line = []
        tf = []

        for i in range(0, width):
            line.append(format(maze[i][j].walls & 0xF, "x"))
            tf.append(f" [{maze[i][j].visited}] ")

        print(f'"{"".join(line)}"')
        # print(f'"{"".join(tf)}"')
        maze_str.append("".join(line))

    return maze_str

"""
This file contains utils functions which are useful
during our converting process

"""
from maze_types import Cell, Direction
import random
from typing import Optional
from dev import show_wall_after_changes


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


def create_and_display_maze(
    maze: list[list[Cell]],
    height: int,
    width: int
) -> tuple[str]:
    maze_str = []

    print("Our maze:")
    for j in range(height - 1, -1, -1):
        line = []

        for i in range(0, width):
            line.append(format(maze[i][j].walls & 0xF, "x"))

        print(f'"{"".join(line)}"')
        maze_str.append("".join(line))

    return maze_str


def make_maze_imperfect(
    maze: list[list[Cell]],
    height: int,
    width: int
) -> list[str]:
    """
    This function randomly destroys walls inside a maze
    to makes it imperfect

    Each iteration alters one cell inside single 3x3 square
    inside the maze

    """
    start_y: int = height - 1
    end_y: int = height - 3
    count_changes: int = 0

    while end_y >= 0:
        start_x: int = 0
        end_x: int = 2

        while end_x < width:
            x = random.randint(start_x, end_x)
            y = random.randint(end_y, start_y)

            # It secures the 42 sign
            if maze[x][y].walls == 15:
                continue

            """
            directions indexes:
            0 - North, 1 - East, 2 - South, 3 - West

            """
            directions: list[int] = [
                maze[x][y].walls & mask for mask in (1, 2, 4, 8)
            ]
            directions_cpy = directions.copy()

            print("Before: ")
            print(directions_cpy)

            if x == 0 or directions_cpy[3] == 0:
                directions.remove(directions_cpy[3])

            if x == width - 1 or directions_cpy[1] == 0:
                directions.remove(directions_cpy[1])

            if y == height - 1 or directions_cpy[0] == 0:
                directions.remove(directions_cpy[0])

            if y == 0 or directions_cpy[2] == 0:
                directions.remove(directions_cpy[2])

            print("After:")
            print(directions_cpy)

            if not directions:
                continue

            picked_wall = random.choice(directions)
            maze[x][y].walls -= picked_wall

            show_wall_after_changes(maze[x][y], picked_wall, x, y)

            start_x += 3
            end_x += 3
            count_changes += 1

        start_y -= 3
        end_y -= 3

    print(f"Changes: {count_changes}\n")

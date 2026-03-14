"""
This file is directly responisble for generating an output

"""

from errors import MazeSizeError
from maze_types import Cell
from utils import random_direction

if __name__ == "__main__":

    maze: list[list[Cell]] = []

    while True:
        try:
            width: int = int(input("Width: "))
            height: int = int(input("Height: "))

            if width < 10 or height < 10:
                raise MazeSizeError("The size of the maze is too small")

            break

        except (MazeSizeError, ValueError) as e:
            print(e)

    # Filling our maze with full cells
    maze: list[list[Cell]] = [
        [Cell(y * width + x) for x in range(width)] for y in range(height)
    ]

    # Our maze generation will start from (0, 0) position
    x = 0
    y = 0

    """
    Each loop have to find nerby positions which is not visited yet
    and randomly pick one of them.

    After that it deletes a path between current position and the picked
    one.
    """

    saved: Cell | None = None
    count = 0
    while x * y >= count:

        direction = random_direction(maze, width, height, x, y)

        maze[x][y].visited = True

        print(direction.value)
        break

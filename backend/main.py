"""
This file is directly responisble for generating an output

"""

from errors import MazeSizeError
from maze_types import Cell
from utils import pick_direction, change_position, remove_wall_at_cell

if __name__ == "__main__":

    maze: list[list[Cell]] = []

    while True:
        try:
            width: int = int(input("Width: "))
            height: int = int(input("Height: "))

            if width < 10 or height < 10:
                raise MazeSizeError("The size of a maze is too small (min 10)")

            if width > 50 or height > 50:
                raise MazeSizeError("The size of a maze is too big (max 50)")

            break

        except (MazeSizeError, ValueError) as e:
            print(e)

    """Filling our maze with full cells"""
    maze: list[list[Cell]] = [
        [Cell(y * width + x) for x in range(width)] for y in range(height)
    ]

    """
    Our generation starts at (0, 0) postition
    saved is a last position which had a choice

    """
    x = 0
    y = 0
    saved: Cell | None = None
    count = 0

    # Musimy odwiedzić górne, dolne, prawe oraz lewe i zmienić
    while width * height >= count:

        """
        direction: indicates which axis we use (x or y)
        go_or_back: (1 or -1) which indicates where we go
        wall: it shows which wall is to destroy

        """

        direction, go_or_back, wall = pick_direction(
            maze,
            width,
            height,
            x,
            y
        )
        go_or_back = int(go_or_back)
        wall = int(wall)

        maze[x][y].visited = True
        maze[x][y].number -= int(wall)
        count += 1

        print(f"\nDirection: {direction}")
        print(f"Go or back: {go_or_back}")
        print(f"Wall: {wall}")

        change_position(direction, go_or_back, x, y)
        remove_wall_at_cell(maze[x][y], wall)

        print(f"Current position: (x: {x}, y: {y})")

        if (count == 3):
            break

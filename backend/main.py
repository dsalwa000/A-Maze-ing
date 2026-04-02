"""
This file is directly responisble for generating an output

"""

from errors import MazeSizeError
from maze_types import Cell
from utils import (
    avaiable_directions,
    change_position,
    pick_direction,
    remove_wall_at_next_cell,
    create_and_display_maze,
)
from dev import (
    maze_direction_details,
    display_wall,
    display_wall_to_destroy,
)

if __name__ == "__main__":

    maze: list[list[Cell]] = []

    while True:
        try:
            width: int = int(input("Width: "))
            height: int = int(input("Height: "))

            if width < 5 or height < 5:
                raise MazeSizeError("The size of a maze is too small (min 10)")

            if width > 50 or height > 50:
                raise MazeSizeError("The size of a maze is too big (max 50)")

            break

        except (MazeSizeError, ValueError) as e:
            print(e)

    """Filling our maze with full cells"""
    maze: list[list[Cell]] = [
        [Cell(y * width + x) for y in range(height)] for x in range(width)
    ]

    """
    Our generation starts at (0, 0) postition
    saved is a last position which had a choice

    """
    x = 0
    y = 0
    saved_positions: list[tuple[int]] = []
    count = 1

    while width * height > count:

        maze[x][y].visited = True

        directions_to_pick = avaiable_directions(
            maze,
            width,
            height,
            x,
            y
        )
        picked_direction = pick_direction(directions_to_pick)

        if picked_direction is None:

            print(f"Saved positions: {saved_positions}")

            for position in saved_positions:
                saved_x, saved_y = position

                direction_check = avaiable_directions(
                    maze,
                    width,
                    height,
                    saved_x,
                    saved_y
                )
                if direction_check:
                    # print("We had it")
                    x = saved_x
                    y = saved_y
                    break

            # print("goin back")
            continue

        """
        direction: indicates which axis we use (x or y)
        go_or_back: (1 or -1) which indicates where we go
        wall: it shows which wall is to destroy

        """
        parts, to_save = picked_direction

        direction, go_or_back, wall_to_destroy = parts
        go_or_back = int(go_or_back)
        wall_to_destroy = int(wall_to_destroy)

        print("Wall before being destroyed: ")
        display_wall(maze[x][y])

        maze[x][y].walls -= wall_to_destroy
        count += 1

        display_wall_to_destroy(wall_to_destroy)
        # display_position(x, y)

        print("Wall after being destroyed:")
        display_wall(maze[x][y])

        if to_save is True:
            saved_positions.insert(0, (x, y))

        x, y = change_position(direction, go_or_back, x, y)
        remove_wall_at_next_cell(maze[x][y], wall_to_destroy)

        maze_direction_details(
            direction,
            go_or_back,
            x, y,
            count
        )

        print()

    print("\nOur maze:")
    maze_str = create_and_display_maze(maze, height, width)

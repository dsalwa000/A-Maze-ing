"""
This file is directly responisble for generating an output

"""

# from errors import MazeSizeError
from mazegen.backend.maze_types import Cell
from mazegen.backend.utils import (
    generate_maze,
    generate_42,
    avaiable_directions,
    change_position,
    pick_direction,
    remove_wall_at_next_cell,
    create_final_string,
    make_maze_imperfect,
)


def maze_numbers_generator(
    width: int,
    height: int,
    is_perfect: bool
) -> list[str]:
    """
    This function randomly create a list of numbers which indicates how walls
    should be displayed.

    """

    maze: list[list[Cell]] = generate_maze(width, height)
    cells_42_amount: int = generate_42(width, height, maze)

    """
    Our generation starts at (0, 0) postition and
    saved_positions are last positions which had a choice

    """
    x = 0
    y = 0
    saved_positions: list[tuple[int, int]] = []
    count = 1

    while (width * height) - cells_42_amount > count:

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
                    x = saved_x
                    y = saved_y
                    break
                else:
                    saved_positions.remove(position)
            continue

        """
        direction: indicates which axis we use (x or y)
        go_or_back: (1 or -1) which indicates where we go
        wall_to_destroy: it shows a bitmark number of wall to destroy

        """
        parts, to_save = picked_direction

        direction, go_or_back, wall_to_destroy = parts

        maze[x][y].walls -= int(wall_to_destroy)
        count += 1

        if to_save is True:
            saved_positions.insert(0, (x, y))

        x, y = change_position(direction, int(go_or_back), x, y)
        remove_wall_at_next_cell(maze[x][y], int(wall_to_destroy))

    if is_perfect is False:
        make_maze_imperfect(maze, height, width)

    return create_final_string(maze, height, width)

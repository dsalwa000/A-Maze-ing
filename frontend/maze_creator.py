from mlx import Mlx
from backend.shortest_path import find_shortest_path
from backend.numbers_generator import maze_numbers_generator

WALL_COLOR = 4294901760  # red
DARK_BG = 0
BLUE_BG = 4278190335


def my_mlx_pixel_put(img_data: tuple[memoryview, int, int, int], x: int,
                     y: int, color: int):
    """Color a pixel

    Arguments:
    img_data -- tuple containing image information
    x and y -- coordinates of the pixel
    color -- color for the pixel
    """
    addr = img_data[0]
    bits_per_pixel = img_data[1]
    line_length = img_data[2]
    offset = int(y * line_length + x * (bits_per_pixel / 8))
    addr[offset] = color % 256
    addr[offset + 1] = (color >> 8) % 256
    addr[offset + 2] = (color >> 16) % 256
    addr[offset + 3] = (color >> 24) % 256


def has_north(code: int):
    """Check if cell with a given code has north wall"""
    if code % 2:
        return True
    else:
        return False


def has_south(code: int):
    """Check if cell with a given code has south wall"""
    if (code >> 2) % 2:
        return True
    else:
        return False


def has_east(code: int):
    """Check if cell with a given code has east wall"""
    if (code >> 1) % 2:
        return True
    else:
        return False


def has_west(code: int):
    """Check if cell with a given code has west wall"""
    if (code >> 3) % 2:
        return True
    else:
        return False


def draw_wall(data, start, end):
    """draw a wall on coordinates from start to end

    Arguments:
    data -- image information
    start -- top left coordinate of the wall
    end -- bottom right coordinate of the wall

    """
    for x in range(start[0], end[0]):
        for y in range(start[1], end[1]):
            my_mlx_pixel_put(data, x, y, WALL_COLOR)


def draw_cell(data, code: int):
    """Draw all walls in a cell

    Arguments:
    data -- image information
    code -- value from 0 to 15 describing the cell's walls

    """
    if has_north(code):
        draw_wall(data, (0, 0), (20, 2))
    if has_south(code):
        draw_wall(data, (0, 18), (20, 20))
    if has_east(code):
        draw_wall(data, (18, 0), (20, 20))
    if has_west(code):
        draw_wall(data, (0, 0), (2, 20))


def init_cell(data, color):
    """Initialize a cell with background color

    data -- image information
    color -- background color of the cell
    """
    for x in range(20):
        for y in range(20):
            my_mlx_pixel_put(data, x, y, color)


def generate_pathway(
    start: tuple[int, int],
    path_string: str
) -> list[tuple[int, int]]:
    """
    Create a pathway list from a string

    start -- starting coordinate of the maze
    path_string -- string consisting of letters S, N, W, E describing a path
    to solve the maze
    returns a list of tuples with coordinates of each step on the pathway

    """
    pathway: list[tuple[int, int]] = []
    current_pos: tuple[int, int] = start
    pathway.append(current_pos)

    for i in range(len(path_string)):
        if path_string[i] == 'S':
            current_pos = (current_pos[0], current_pos[1] + 1)
        elif path_string[i] == 'N':
            current_pos = (current_pos[0], current_pos[1] - 1)
        elif path_string[i] == 'W':
            current_pos = (current_pos[0] - 1, current_pos[1])
        elif path_string[i] == 'E':
            current_pos = (current_pos[0] + 1, current_pos[1])
        pathway.append(current_pos)

    return pathway


def create_visualization(
    width: int,
    height: int,
    start: tuple[int, int],
    end: tuple[int, int],
    is_perfect: bool
) -> None:
    """Calls maze generator and creates a visual for the created maze

    Arguments:
    width -- width of the maze
    height -- height of the maze
    start -- entry point of the maze
    end -- exit point of the maze
    is_perfect -- whether the maze is perfect (has one solution) or not

    """
    m = Mlx()
    mlx_ptr = m.mlx_init()
    win_ptr = m.mlx_new_window(mlx_ptr, width * 20, height * 20, "Maze")
    m.mlx_clear_window(mlx_ptr, win_ptr)

    config_list: list[str] = maze_numbers_generator(width, height, is_perfect)
    config: str = "".join(config_list)

    pathway_str: str = find_shortest_path(config, start, end, width, height)
    pathway: list[tuple[int, int]] = generate_pathway(start, pathway_str)

    try:
        with open("output_maze.txt", "w", encoding="utf-8") as file:
            """
            We are writing our final maze configuration inside
            output_maze.txt, how it should looks like:

            d515155513
            954543d56a
            c3f916fffa
            92fc4157fa
            aafffafffa
            a817fafd52
            c6c3fafffa
            953c52953a
            83c3d283aa
            ec5456c6c6

            (0, 0)
            (9, 9)
            EEEEEEEEESSSSSSSSS

            """
            file.writelines(f"{line}\n" for line in config_list)

            file.write(f"\n{start[0], start[1]}\n")
            file.write(f"{end[0], end[1]}\n")
            file.write(pathway_str)

    except Exception as e:
        print(f"Error regarding output_maze.txt file: {e}")

    for i in range(len(config)):
        img = m.mlx_new_image(mlx_ptr, 20, 20)
        img_data = m.mlx_get_data_addr(img)
        x = (i % width)
        y = i // width

        if (x, y) in pathway:
            init_cell(img_data, BLUE_BG)
        else:
            init_cell(img_data, DARK_BG)

        draw_cell(img_data, int(config[i], 16))
        m.mlx_put_image_to_window(mlx_ptr, win_ptr, img, x * 20, y * 20)

    m.mlx_loop(mlx_ptr)

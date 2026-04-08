from mlx import Mlx
from backend.shortest_path import find_shortest_path
from backend.maze_generator import maze_numbers_generator

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


def generate_pathway(start: tuple, path_string: str) -> list:
    """Create a pathway list from a string

    start -- starting coordinate of the maze
    path_string -- string consisting of letters S, N, W, E describing a path
    to solve the maze
    returns a list of tuples with coordinates of each step on the pathway
    """
    pathway = []
    current_pos = start
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


def create_visualization(width: int, height: int, start: int, end: int,
                         is_perfect: bool) -> None:
    m = Mlx()
    mlx_ptr = m.mlx_init()
    win_ptr = m.mlx_new_window(mlx_ptr, width * 20, height * 20, "Maze")
    m.mlx_clear_window(mlx_ptr, win_ptr)

    # config = (
    #     "9515391539551795151151153"
    #     "EBABAE812853C1412BA812812"
    #     "96A8416A84545412AC4282C2A"
    #     "C3A83816A9395384453A82D02"
    #     "96842A852AC07AAD13A8283C2"
    #     "C1296C43AAB83AA92AA8686BA"
    #     "92E853968428444682AC12902"
    #     "AC3814452FA83FFF82C52C42A"
    #     "85684117AFC6857FAC1383D06"
    #     "C53AD043AFFFAFFF856AA8143"
    #     "91441294297FAFD501142C6BA"
    #     "AA912AC3843FAFFF82856D52A"
    #     "842A8692A92B8517C4451552A"
    #     "816AC384468285293917A9542"
    #     "C416928513C443A828456C3BA"
    #     "91416AA92C393A82801553AAA"
    #     "A81292AA814682C6A8693C6AA"
    #     "A8442C6C2C1168552C16A9542"
    #     "86956951692C1455416928552"
    #     "C545545456C54555545444556"
    # )
    config = maze_numbers_generator(width, height, is_perfect)

    # start = (random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
    # end = (random.randrange(0, WIDTH), random.randrange(0, HEIGHT))

    pathway_str = find_shortest_path(config, start, end, width, height)
    pathway = generate_pathway(start, pathway_str)
    # pathway = generate_pathway((1, 1),
    #                            "SWSESWSESWSSSEESEEENEESESEESSSEEESSSEEENNENEE")

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

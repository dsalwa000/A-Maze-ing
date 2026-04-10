from mlx import Mlx
from backend.shortest_path import find_shortest_path
from backend.numbers_generator import maze_numbers_generator
import os

COLOR_RED = 4294901760  # red
# WALL_COLOR = 4278222848
COLOR_GR = 4278255360
COLOR_BL = 4278190335
DARK_BG = 0
PATH_BG = COLOR_BL
COLORS = [COLOR_RED, COLOR_GR, COLOR_BL]


class MazeVisualizer():
    def __init__(self, m, mlx_ptr, win_ptr, width, height, config, start, end, pathway):
        self.m = m
        self.mlx_ptr = mlx_ptr
        self.win_ptr = win_ptr
        self.width = width
        self.height = height
        self.pathway = []
        self.config = config
        self.start = start
        self.end = end
        self.pathway = self.generate_pathway(start, pathway)
        self.color_index = 0
        self.is_drawing = False

    def my_mlx_pixel_put(self, img_data: tuple[memoryview, int, int, int], x: int,
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

    def has_north(self, code: int):
        """Check if cell with a given code has north wall"""
        if code % 2:
            return True
        else:
            return False

    def has_south(self, code: int):
        """Check if cell with a given code has south wall"""
        if (code >> 2) % 2:
            return True
        else:
            return False

    def has_east(self, code: int):
        """Check if cell with a given code has east wall"""
        if (code >> 1) % 2:
            return True
        else:
            return False

    def has_west(self, code: int):
        """Check if cell with a given code has west wall"""
        if (code >> 3) % 2:
            return True
        else:
            return False

    def draw_wall(self, data, start, end):
        """draw a wall on coordinates from start to end

        Arguments:
        data -- image information
        start -- top left coordinate of the wall
        end -- bottom right coordinate of the wall
        """
        for x in range(start[0], end[0]):
            for y in range(start[1], end[1]):
                self.my_mlx_pixel_put(data, x, y, COLORS[self.color_index])

    def draw_cell(self, data, code: int):
        """Draw all walls in a cell

        Arguments:
        data -- image information
        code -- value from 0 to 15 describing the cell's walls
        """
        if self.has_north(code):
            self.draw_wall(data, (0, 0), (20, 2))
        if self.has_south(code):
            self.draw_wall(data, (0, 18), (20, 20))
        if self.has_east(code):
            self.draw_wall(data, (18, 0), (20, 20))
        if self.has_west(code):
            self.draw_wall(data, (0, 0), (2, 20))

    def init_cell(self, data, color):
        """Initialize a cell with background color

        data -- image information
        color -- background color of the cell
        """
        for x in range(20):
            for y in range(20):
                self.my_mlx_pixel_put(data, x, y, color)

    def generate_pathway(self, start: tuple, path_string: str) -> list:
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
        self.pathway = pathway
        return pathway

    def draw_cells(self, draw_path: bool):
        self.is_drawing = True
        for i in range(len(self.config)):
            img = self.m.mlx_new_image(self.mlx_ptr, 20, 20)
            img_data = self.m.mlx_get_data_addr(img)
            x = (i % self.width)
            y = i // self.width

            if draw_path and (x, y) in self.pathway:
                self.init_cell(img_data, PATH_BG)
            else:
                self.init_cell(img_data, DARK_BG)

            self.draw_cell(img_data, int(self.config[i], 16))
            self.m.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, img, x * 20, y * 20)
        self.is_drawing = False

    def change_color(self):
        self.color_index += 1
        if self.color_index >= len(COLORS):
            self.color_index = 0


def key_hook(keycode: int, param) -> None:
    if keycode == 49:
        print("user selected 1")
    elif keycode == 50:
        print("user selected 2")
    elif keycode == 51:
        if param["visualizer"].is_drawing is False:
            param["visualizer"].change_color()
            param["visualizer"].draw_cells(True)
    if keycode == 52:
        param["m"].mlx_destroy_window(param["mlx"], param["win"])
        os._exit(0)
    if keycode == 65307:  # ESC (Linux)
        os._exit(0)


def create_visualization(width: int, height: int, start: int, end: int,
                         is_perfect: bool) -> None:
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

    visualizer = MazeVisualizer(m, mlx_ptr, win_ptr, width, height, config, start, end, pathway_str)

    visualizer.draw_cells(True)

    data = {"m": m, "mlx": mlx_ptr, "win": win_ptr, "visualizer": visualizer}

    m.mlx_key_hook(win_ptr, key_hook, data)

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

    m.mlx_loop(mlx_ptr)

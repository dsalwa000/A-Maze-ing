from mlx import Mlx
from MazeGenerator import MazeGenerator
import os

COLOR_RED = 4294901760
COLOR_GR = 4278255360
COLOR_BL = 4278190335
COLOR_BRIGHT_BL = 4278215935
COLOR_WHITE = 4294967295
DARK_BG = 4278190080
PATH_BG = COLOR_BRIGHT_BL
FT_COLOR = COLOR_WHITE
COLORS = [COLOR_RED, COLOR_GR, COLOR_BL]
CELL_SIZE = 20


class MazeVisualizer():
    def __init__(
        self,
        m,
        mlx_ptr,
        win_ptr,
        width,
        height,
        config,
        start,
        end,
        pathway,
    ):
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
        self.draw_path = True
        self.color_forty_two = False
        self.img_red = None
        self.img_green = None
        self.img_blue = None
        self.images = []
        self.gen_images()

    def my_mlx_pixel_put(
        self,
        img_data: tuple[memoryview, int, int, int],
        x: int,
        y: int,
        color: int,
    ):
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

    def draw_wall(self, data, start, end, cell_pos: tuple[int, int], color):
        """draw a wall on coordinates from start to end

        Arguments:
        data -- image information
        start -- top left coordinate of the wall
        end -- bottom right coordinate of the wall
        """
        for x in range(
            start[0] + cell_pos[0] * CELL_SIZE,
            end[0] + cell_pos[0] * CELL_SIZE,
        ):
            for y in range(
                start[1] + cell_pos[1] * CELL_SIZE,
                end[1] + cell_pos[1] * CELL_SIZE,
            ):
                self.my_mlx_pixel_put(data, x, y, color)

    def draw_cell(self, data, code: int, cell_pos: tuple[int, int], color):
        """Draw all walls in a cell

        Arguments:
        data -- image information
        code -- value from 0 to 15 describing the cell's walls
        """
        if self.has_north(code):
            self.draw_wall(
                data,
                (0, 0),
                (CELL_SIZE, CELL_SIZE // 10),
                cell_pos,
                color,
            )
        if self.has_south(code):
            self.draw_wall(
                data,
                (0, CELL_SIZE - CELL_SIZE // 10),
                (CELL_SIZE, CELL_SIZE),
                cell_pos,
                color,
            )
        if self.has_east(code):
            self.draw_wall(
                data,
                (CELL_SIZE - CELL_SIZE // 10, 0),
                (CELL_SIZE, CELL_SIZE),
                cell_pos,
                color,
            )
        if self.has_west(code):
            self.draw_wall(
                data,
                (0, 0),
                (CELL_SIZE // 10, CELL_SIZE),
                cell_pos,
                color,
            )

    def init_cell(self, data, color, cell_pos: tuple[int, int]):
        """Initialize a cell with background color

        data -- image information
        color -- background color of the cell
        """
        for x in range(CELL_SIZE):
            for y in range(CELL_SIZE):
                self.my_mlx_pixel_put(
                    data,
                    x + cell_pos[0] * CELL_SIZE,
                    y + cell_pos[1] * CELL_SIZE,
                    color,
                )

    def generate_pathway(self, start: tuple, path_string: str) -> list:
        """
        Create a pathway list from a string

        start -- starting coordinate of the maze
        path_string -- string consisting of letters S, N, W, E describing
        a path to solve the maze
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

    def draw_cells(self, img_data, color):
        for i in range(len(self.config)):
            x = (i % self.width)
            y = i // self.width

            if self.draw_path and (x, y) in self.pathway:
                self.init_cell(img_data, PATH_BG, (x, y))

            self.draw_cell(img_data, int(self.config[i], 16), (x, y), color)

    def put_image(self):
        self.m.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.images[self.color_index],
            0,
            0
        )

    def gen_images(self):
        self.img_red = self.m.mlx_new_image(
            self.mlx_ptr,
            self.width * CELL_SIZE,
            self.height * CELL_SIZE,
        )
        self.img_green = self.m.mlx_new_image(
            self.mlx_ptr,
            self.width * CELL_SIZE,
            self.height * CELL_SIZE,
        )
        self.img_blue = self.m.mlx_new_image(
            self.mlx_ptr,
            self.width * CELL_SIZE,
            self.height * CELL_SIZE,
        )
        img_data_r = self.m.mlx_get_data_addr(self.img_red)
        img_data_g = self.m.mlx_get_data_addr(self.img_green)
        img_data_b = self.m.mlx_get_data_addr(self.img_blue)

        self.images = [self.img_red, self.img_green, self.img_blue]

        self.draw_cells(img_data_r, COLOR_RED)
        self.draw_cells(img_data_g, COLOR_GR)
        self.draw_cells(img_data_b, COLOR_BL)

    def change_color(self):
        self.color_index += 1
        if self.color_index >= len(COLORS):
            self.color_index = 0

    def redraw_pathway(self) -> None:
        for j in range(len(self.images)):
            current_img = self.images[j]
            img_data = self.m.mlx_get_data_addr(current_img)
            for i in range(len(self.config)):

                x = (i % self.width)
                y = i // self.width

                if (x, y) in self.pathway:
                    if self.draw_path:
                        self.init_cell(img_data, PATH_BG, (x, y))
                    else:
                        self.init_cell(img_data, DARK_BG, (x, y))

                    self.draw_cell(
                        img_data,
                        int(self.config[i], 16),
                        (x, y),
                        COLORS[j]
                    )

        self.m.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.images[self.color_index],
            0,
            0
        )

    def recolor_forty_two(self):
        for j in range(len(self.images)):
            current_img = self.images[j]
            img_data = self.m.mlx_get_data_addr(current_img)
            for i in range(len(self.config)):

                x = (i % self.width)
                y = i // self.width

                if int(self.config[i], 16) == 15:
                    if self.color_forty_two:
                        self.init_cell(img_data, FT_COLOR, (x, y))
                    else:
                        self.init_cell(img_data, DARK_BG, (x, y))

                    self.draw_cell(
                        img_data,
                        int(self.config[i], 16),
                        (x, y),
                        COLORS[j]
                    )
        self.m.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.images[self.color_index],
            0,
            0
        )

    def regenerate_maze(self):
        g = MazeGenerator()
        self.config = g.config
        self.pathway = self.generate_pathway(g.entry, g.shortest_path)
        self.start = g.entry
        self.end = g.exit
        self.width = g.width
        self.height = g.height
        self.gen_images()
        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.put_image()
        g.render_to_file()


def key_hook(keycode: int, param) -> None:
    if keycode == 49:
        param["visualizer"].regenerate_maze()
    elif keycode == 50:
        param["visualizer"].draw_path = not param["visualizer"].draw_path
        param["visualizer"].redraw_pathway()
    elif keycode == 51:
        param["visualizer"].change_color()
        param["visualizer"].put_image()
    elif keycode == 52:
        param["visualizer"].color_forty_two = (
            not param["visualizer"].color_forty_two
        )
        param["visualizer"].recolor_forty_two()
    elif keycode == 53 or keycode == 65307:
        param["m"].mlx_destroy_window(param["mlx"], param["win"])
        os._exit(0)


def create_visualization(
    width: int,
    height: int,
    start: int,
    end: int,
    config_list: list[str],
    pathway_str: str
) -> None:
    """
    Calls maze generator and creates a visual for the created maze

    Arguments:
    width -- width of the maze
    height -- height of the maze
    start -- entry point of the maze
    end -- exit point of the maze
    is_perfect -- whether the maze is perfect (has one solution) or not

    """
    try:
        m = Mlx()
        mlx_ptr = m.mlx_init()
        win_ptr = m.mlx_new_window(
            mlx_ptr,
            width * CELL_SIZE,
            height * CELL_SIZE,
            "Maze"
        )
        m.mlx_clear_window(mlx_ptr, win_ptr)

        config: str = "".join(config_list)

        visualizer = MazeVisualizer(
            m,
            mlx_ptr,
            win_ptr,
            width,
            height,
            config,
            start,
            end,
            pathway_str
        )

        visualizer.put_image()

        data = {
            "m": m,
            "mlx": mlx_ptr,
            "win": win_ptr,
            "visualizer": visualizer
        }

        m.mlx_key_hook(win_ptr, key_hook, data)
        m.mlx_loop(mlx_ptr)

    except Exception as e:
        print(f"Error while drawing the maze: {e}")

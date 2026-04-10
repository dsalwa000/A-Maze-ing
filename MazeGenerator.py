"""
It is a stanalone module which allows you to generates the maze

"""
from backend.numbers_generator import maze_numbers_generator
from backend.errors import MazeSizeError, MazeParamsError
from frontend.maze_creator import create_visualization
from backend.shortest_path import find_shortest_path
from a_maze_ing import parce_params, check_final_params, check_maze_possibility
import random
import sys


class MazeGenerator:
    """
    So here we go, the best maze in the world!
    (If the rest of the mazes don't exist)

    """
    def __init__(self) -> None:
        self.params: dict = None

        try:
            if len(sys.argv) != 2:
                print("error")
            else:
                with open(sys.argv[1], "r") as f:
                    contents = f.read()

                    contents_list = contents.split("\n")
                    contents_list = [x for x in contents_list if x[0] != '#']
                    params_unprocessed: dict[str, str] = {
                        x.split("=")[0]: x.split("=")[1] for x in contents_list
                    }
                    self.params: dict = parce_params(params_unprocessed)

                    if not check_final_params(self.params):
                        raise MazeParamsError
                    check_maze_possibility(self.params)

        except FileNotFoundError:
            print("ERROR: Config file not found")
        except IndexError:
            print("ERROR: Wrong format in config file")
            print("Each line should be KEY=VALUE")
            print("Comments are allowed and should start with '#'")
        except MazeParamsError:
            print("Params are incorrect")
        except MazeSizeError:
            print("ERROR: bad maze size, or entry and exit are out of bounds")
        except Exception as e:
            print(f"An unexpected error occured: {e}")

        self.width: int = self.params["WIDTH"]
        self.height: int = self.params["HEIGHT"]
        self.entry: tuple[int, int] = self.params["ENTRY"]
        self.exit: tuple[int, int] = self.params["EXIT"]
        self.is_perfect: bool = self.params["PERFECT"]

        random.seed(self.params["SEED"])

        config_str: list[str] = maze_numbers_generator(
            self.width,
            self.height,
            self.is_perfect
        )
        self.config: str = "".join(config_str)

        # Here we have a problem
        self.shortest_path: str = find_shortest_path(
            self.config,
            self.entry,
            self.exit,
            self.width,
            self.height
        )

    def render_maze(self) -> None:
        create_visualization(
            self.width,
            self.height,
            self.entry,
            self.exit,
            self.config,
            self.shortest_path
        )

    def display_maze_settings(self) -> None:
        print(f"{line}\n" for line in self.config_str)

        print(f"\n{self.entry[0], self.entry[1]}\n")
        print(f"{self.exit[0], self.exit[1]}\n")
        print(self.shortest_path)


if __name__ == "__main__":
    """
    Let's test

    """
    maze_generator = MazeGenerator()

    maze_generator.render_maze()

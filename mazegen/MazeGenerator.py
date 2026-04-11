"""
It is a stanalone module which allows you to generates the maze

"""
from mazegen.backend.numbers_generator import maze_numbers_generator
from mazegen.backend.errors import MazeSizeError, MazeParamsError
from mazegen.backend.shortest_path import find_shortest_path
from mazegen.utils import (
    parce_params,
    check_final_params,
    check_maze_possibility
)
import random
import sys


class MazeGenerator:
    """
    So here we go, the best maze in the world!
    (If the rest of the mazes don't exist)

    """
    def __init__(self) -> None:
        self.params: dict = {}

        if len(sys.argv) != 2:
            raise MazeParamsError("There is no config file!")
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
                    raise MazeParamsError("Params are incorrect")
                check_maze_possibility(self.params)

        if self.params["WIDTH"] < 10 or self.params["HEIGHT"] < 10:
            raise MazeSizeError(
                "The maze is to small! Min size is 10 x 10"
            )

        if self.params["ENTRY"] == self.params["EXIT"]:
            raise MazeParamsError(
                "The start position and exit positions are the same.\n"
                "Fix it!"
            )

        self.width: int = self.params["WIDTH"]
        self.height: int = self.params["HEIGHT"]
        self.entry: tuple[int, int] = self.params["ENTRY"]
        self.exit: tuple[int, int] = self.params["EXIT"]
        self.is_perfect: bool = self.params["PERFECT"]

        if self.params.get("SEED") is not None:
            random.seed(self.params["SEED"])

        self.config_list: list[str] = maze_numbers_generator(
            self.width,
            self.height,
            self.is_perfect
        )
        self.config: str = "".join(self.config_list)

        # Here we have a problem
        self.shortest_path: str = find_shortest_path(
            self.config,
            self.entry,
            self.exit,
            self.width,
            self.height
        )

    def render_maze(self) -> None:
        from mazegen.frontend.maze_creator import create_visualization
        create_visualization(
            self.width,
            self.height,
            self.entry,
            self.exit,
            self.config,
            self.shortest_path
        )

    def render_to_file(self) -> None:
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
                file.writelines(f"{line}\n" for line in self.config_list)

                file.write(f"\n{self.entry[0], self.entry[1]}\n")
                file.write(f"{self.exit[0], self.exit[1]}\n")
                file.write(self.shortest_path)

        except Exception as e:
            print(f"Error regarding output_maze.txt file: {e}")

    def display_maze_settings(self) -> None:
        for line in self.config_list:
            print(line)

        print(f"\n{self.entry[0], self.entry[1]}")
        print(f"{self.exit[0], self.exit[1]}")
        print(self.shortest_path)

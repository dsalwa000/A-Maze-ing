import sys
from frontend.maze_creator import create_visualization
from backend.errors import MazeSizeError
import random


def parce_params(params_unprocessed: dict[str, str]) -> dict[str, object]:
    """
    Turns values of dict from strings to proper types
    WIDTH and HEIGHT are converted to int, ENTRY and EXIT to
    tuples of ints, PERFECT to boolean, OUTPUT_FILE remains unchanged

    """
    params = {}
    try:
        try:
            params["WIDTH"] = int(params_unprocessed["WIDTH"])
            params["HEIGHT"] = int(params_unprocessed["HEIGHT"])
            params["SEED"] = int(params_unprocessed["SEED"])

        except ValueError:
            print("ERROR: width and height must be integers")

        try:
            params["ENTRY"] = tuple(
                map(lambda x: int(x),
                    params_unprocessed["ENTRY"].split(",")))
            params["EXIT"] = tuple(
                map(lambda x: int(x),
                    params_unprocessed["EXIT"].split(",")))

        except ValueError:
            print("ERROR: entry and exit must be in format 'int,int'")

        try:
            if params_unprocessed["PERFECT"] == "True":
                params["PERFECT"] = True
            elif params_unprocessed["PERFECT"] == "False":
                params["PERFECT"] = False
            else:
                raise ValueError

        except ValueError:
            print("ERROR: 'perfect' must be either 'True' or 'False'")

        try:
            if len(params_unprocessed["OUTPUT_FILE"]) == 0:
                raise ValueError
            else:
                params["OUTPUT_FILE"] = params_unprocessed["OUTPUT_FILE"]

        except ValueError:
            print("ERROR: output_file can not be empty")

    except KeyError:
        print("ERROR: not all necessary values present in config")
        print(
            "Necessary values: WIDTH, HEIGHT, ENTRY, EXIT, PERFECT,"
            " OUTPUT_FILE, SEED"
        )

    return params


def check_final_params(params: dict) -> bool:
    """Check that all parameters for a maze were properly added"""
    required_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    ]
    return all(params.get(key) is not None for key in required_keys)


def check_maze_possibility(params: dict) -> None:
    """Check if maze size is appropriate"""
    if (params["WIDTH"] <= params["ENTRY"][0] or
            params["WIDTH"] <= params["EXIT"][0] or
            params["HEIGHT"] <= params["ENTRY"][1] or
            params["HEIGHT"] <= params["EXIT"][1]):
        raise MazeSizeError


if __name__ == "__main__":
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
                params: dict = parce_params(params_unprocessed)

                if check_final_params(params):
                    random.seed(params["SEED"])
                    check_maze_possibility(params)
                    create_visualization(params["WIDTH"], params["HEIGHT"],
                                         params["ENTRY"], params["EXIT"],
                                         params["PERFECT"])

    except FileNotFoundError:
        print("ERROR: Config file not found")
    except IndexError:
        print("ERROR: Wrong format in config file")
        print("Each line should be KEY=VALUE")
        print("Comments are allowed and should start with '#'")
    except MazeSizeError:
        print("ERROR: bad maze size, or entry and exit are out of bounds")
    except Exception:
        print("An unknown error occured")

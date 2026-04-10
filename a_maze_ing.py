from backend.errors import MazeSizeError


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

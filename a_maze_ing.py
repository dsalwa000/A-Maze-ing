import sys
from frontend.main import create_visualization


def parce_params(params_unprocessed: dict) -> dict:
    """Turns values of dict from strings to proper types
    WIDTH and HEIGHT are converted to int, ENTRY and EXIT to
    tuples of ints, PERFECT to boolean, OUTPUT_FILE remains unchanged
    """
    params = {}
    try:
        try:
            params["WIDTH"] = int(params_unprocessed["WIDTH"])
            params["HEIGHT"] = int(params_unprocessed["HEIGHT"])

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
            " OUTPUT_FILE"
            )
    return params


def check_final_params(params: dict) -> bool:
    if (params.get("WIDTH") is None or
            params.get("HEIGHT") is None or
            params.get("ENTRY") is None or
            params.get("EXIT") is None or
            params.get("OUTPUT_FILE") is None or
            params.get("PERFECT") is None):
        return False
    else:
        return True


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("error")
        else:
            with open(sys.argv[1], "r") as f:
                contents = f.read()
                contents_list = contents.split("\n")
                contents_list = [x for x in contents_list if x[0] != '#']
                params_unprocessed = {x.split("=")[0]: x.split("=")[1] for x
                                      in contents_list}
                params = parce_params(params_unprocessed)
                if check_final_params(params):
                    create_visualization(params["WIDTH"], params["HEIGHT"],
                                         params["ENTRY"], params["EXIT"],
                                         params["PERFECT"])

    except FileNotFoundError:
        print("ERROR: Config file not found")
    except IndexError:
        print("ERROR: Wrong format in config file")
        print("Each line should be KEY=VALUE")
        print("Comments are allowed and should start with '#'")
    except Exception:
        print("An unknown error occured")

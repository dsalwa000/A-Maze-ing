import sys
from frontend.main import create_visualization


def parce_params(params_unprocessed: dict) -> dict:
    """Turns values of dict from strings to proper types
    WIDTH and HEIGHT are converted to int, ENTRY and EXIT to
    tuples of ints, PERFECT to boolean, OUTPUT_FILE remains unchanged
    """
    params = {}
    params["WIDTH"] = int(params_unprocessed["WIDTH"])
    params["HEIGHT"] = int(params_unprocessed["HEIGHT"])
    params["ENTRY"] = tuple(map(lambda x: int(x),
                                params_unprocessed["ENTRY"].split(",")))
    params["EXIT"] = tuple(map(lambda x: int(x),
                               params_unprocessed["EXIT"].split(",")))
    if params_unprocessed["PERFECT"] == "True":
        params["PERFECT"] = True
    elif params_unprocessed["PERFECT"] == "False":
        params["PERFECT"] = False
    return params


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("error")
        else:
            with open(sys.argv[1], "r") as f:
                contents = f.read()
                contents_list = contents.split("\n")
                params_unprocessed = {x.split("=")[0]: x.split("=")[1] for x
                                      in contents_list}
                params = parce_params(params_unprocessed)
                print(params)
                create_visualization(params["WIDTH"], params["HEIGHT"],
                                     params["ENTRY"], params["EXIT"],
                                     params["PERFECT"])

    except FileNotFoundError:
        print("ERROR: Config file not found")

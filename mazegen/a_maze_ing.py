from mazegen.MazeGenerator import MazeGenerator
from mazegen.backend.errors import MazeSizeError, MazeParamsError

if __name__ == "__main__":
    """
    Let's test

    """
    try:
        maze_generator = MazeGenerator()

        maze_generator.render_to_file()
        maze_generator.display_maze_settings()
        maze_generator.render_maze()

    except FileNotFoundError:
        print("ERROR: Config file not found")
    except IndexError:
        print("ERROR: Wrong format in config file")
        print("Each line should be KEY=VALUE")
        print("Comments are allowed and should start with '#'")
    except (MazeSizeError, MazeParamsError) as e:
        print(f"Maze error occured: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")

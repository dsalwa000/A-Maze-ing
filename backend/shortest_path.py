from __future__ import annotations


class Cell:
    """Class containing information about a cell
    value -- number from 0 to 15, specifying what walls the cell has
    position -- a tuple containing x and y coordinates of a cell
    maze_width -- total width of the maze
    maze_height -- total height of the maze
    """
    def __init__(self, value: str, position: tuple, maze_width: int,
                 maze_height: int) -> None:
        self.value: int = int(value, 16)
        self.position: tuple = position
        self.distance: int = 0
        self.caller: Cell = None
        self.is_visited: bool = False
        self.maze_width = maze_width
        self.maze_height = maze_height

    def add_to_queue(self, caller: 'Cell') -> None:
        """When added to the queue by the previous cell (caller), change
        internal properties where needed
        """
        self.caller = caller
        self.distance = caller.distance + 1
        self.is_visited = True

    def north(self, graph: list) -> Cell | None:
        """Get a cell to north of self if it can be entered, return None
        otherwise
        """
        if self.position[1] > 0 and not self.value % 2:
            return get_cell_at_pos(graph,
                                   (self.position[0],
                                    self.position[1] - 1),
                                   self.maze_width)
        else:
            return None

    def south(self, graph: list) -> Cell | None:
        """Get a cell to south of self if it can be entered, return None
        otherwise
        """
        if (
            self.position[1] < self.maze_height - 1 and
            not (self.value >> 2) % 2
        ):
            return get_cell_at_pos(graph,
                                   (self.position[0],
                                    self.position[1] + 1),
                                   self.maze_width)
        else:
            return None

    def east(self, graph: list) -> Cell | None:
        """Get a cell to east of self if it can be entered, return None
        otherwise
        """
        if (
            self.position[0] < self.maze_width - 1 and
            not (self.value >> 1) % 2
        ):
            return get_cell_at_pos(graph,
                                   (self.position[0] + 1,
                                    self.position[1]),
                                   self.maze_width)
        else:
            return None

    def west(self, graph: list) -> Cell | None:
        """Get a cell to west of self if it can be entered, return None
        otherwise
        """
        if self.position[0] > 0 and not (self.value >> 3) % 2:
            return get_cell_at_pos(graph,
                                   (self.position[0] - 1,
                                    self.position[1]),
                                   self.maze_width)
        else:
            return None


def get_available_neighbours(graph: list, cell: Cell) -> set:
    """Get all the neighboring cells that are not blocked by a wall and haven't
    been visited

    Arguments:
    graph -- list of all cells in proper order
    cell -- a cell whose neighbours we are scanning
    """
    res = set()

    north = cell.north(graph)
    if north is not None and not north.is_visited:
        res.add(north)
    south = cell.south(graph)
    if south is not None and not south.is_visited:
        res.add(south)
    east = cell.east(graph)
    if east is not None and not east.is_visited:
        res.add(east)
    west = cell.west(graph)
    if west is not None and not west.is_visited:
        res.add(west)

    return res


def make_step(graph: list, queue: list) -> list:
    """One step in the algorithm - get all available neighbours for each cell
    in current queue, and make them the next queue

    Arguments:
    graph -- list of all cells in proper order
    queue -- list of cells that we are currently in
    """
    new_queue = []
    for cell in queue:
        neighbours = get_available_neighbours(graph, cell)
        for n in neighbours:
            new_queue.append(n)
            n.add_to_queue(cell)
    return new_queue


def parse_path(path: list) -> str:
    """Get a string describing a path from a list of cells

    Arguments:
    path -- the list of cells
    """
    path_str = ""
    for i in range(1, len(path)):
        if path[i].position[0] > path[i - 1].position[0]:
            path_str += "E"
        elif path[i].position[0] < path[i - 1].position[0]:
            path_str += "W"
        elif path[i].position[1] > path[i - 1].position[1]:
            path_str += "S"
        elif path[i].position[1] < path[i - 1].position[1]:
            path_str += "N"
    return path_str


def get_cell_at_pos(graph: list, pos: tuple, maze_width: int) -> Cell:
    """Get a cell in the maze based on its' position

    Arguments:
    graph -- list of all cells in proper order
    pos -- tuple with x and y values of the cell
    maze_width -- total width of the maze
    """
    i = pos[1] * maze_width + pos[0]
    return graph[i]


def find_shortest_path(config: str, start: tuple, end: tuple, maze_width: int,
                       maze_height: int) -> str:
    """Find the shortest path in the maze described by the config string

    Arguments:
    config -- the string describing the maze
    start -- start position
    end -- end position
    maze_width -- total width of the maze
    maze_height -- total height of the maze
    """

    graph = []
    for i in range(len(config)):
        cell = Cell(config[i], (i % maze_width, i // maze_width), maze_width,
                    maze_height)
        graph.append(cell)

    queue = []
    queue.append(get_cell_at_pos(graph, start, maze_width))

    finish = None

    while len(queue) > 0:
        queue = make_step(graph, queue)
        finish = next((x for x in queue if x.position == end), None)
        if finish is not None:
            break

    if finish is not None:
        print(f"Successfully found finish at {finish.position}")
        print("Our path:")

        cell = finish
        path_cells = []
        while cell.position != start:
            path_cells.append(cell)
            cell = cell.caller
        path_cells.append(cell)

        path_cells.reverse()

        pathway = parse_path(path_cells)
        return pathway

    else:
        print("Didnt find finish")
        return None

MAZE_SIZE = 25


class Cell:
    """Class containing information about a cell"""
    def __init__(self, value, position):
        self.value = int(value, 16)
        self.position = position
        self.distance = 0
        self.caller = None
        self.is_visited = False

    def add_to_queue(self, caller):
        """When added to the queue by the previous cell (caller), change
        internal properties where needed
        """
        self.caller = caller
        self.distance = caller.distance + 1
        self.is_visited = True

    def north(self, graph):
        """Get a cell to north of self if it can be entered, return None
        otherwise
        """
        if self.position[1] <= MAZE_SIZE and not self.value % 2:
            return get_cell_at_pos(graph, (self.position[0],
                                           self.position[1] - 1))
        else:
            return None

    def south(self, graph):
        """Get a cell to south of self if it can be entered, return None
        otherwise
        """
        if self.position[1] >= 0 and not (self.value >> 2) % 2:
            return get_cell_at_pos(graph, (self.position[0],
                                           self.position[1] + 1))
        else:
            return None

    def east(self, graph):
        """Get a cell to east of self if it can be entered, return None
        otherwise
        """
        if self.position[0] <= MAZE_SIZE and not (self.value >> 1) % 2:
            return get_cell_at_pos(graph, (self.position[0] + 1,
                                           self.position[1]))
        else:
            return None

    def west(self, graph):
        """Get a cell to west of self if it can be entered, return None
        otherwise
        """
        if self.position[0] >= 0 and not (self.value >> 3) % 2:
            return get_cell_at_pos(graph, (self.position[0] - 1,
                                           self.position[1]))
        else:
            return None


def get_available_neighbours(graph, cell):
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


def make_step(graph, queue):
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


def parse_path(path):
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


def get_cell_at_pos(graph, pos):
    """Get a cell in the maze based on its' position

    Arguments:
    graph -- list of all cells in proper order
    pos -- tuple with x and y values of the cell
    """
    i = pos[1] * MAZE_SIZE + pos[0]
    return graph[i]


config = (
    "9515391539551795151151153"
    "EBABAE812853C1412BA812812"
    "96A8416A84545412AC4282C2A"
    "C3A83816A9395384453A82D02"
    "96842A852AC07AAD13A8283C2"
    "C1296C43AAB83AA92AA8686BA"
    "92E853968428444682AC12902"
    "AC3814452FA83FFF82C52C42A"
    "85684117AFC6857FAC1383D06"
    "C53AD043AFFFAFFF856AA8143"
    "91441294297FAFD501142C6BA"
    "AA912AC3843FAFFF82856D52A"
    "842A8692A92B8517C4451552A"
    "816AC384468285293917A9542"
    "C416928513C443A828456C3BA"
    "91416AA92C393A82801553AAA"
    "A81292AA814682C6A8693C6AA"
    "A8442C6C2C1168552C16A9542"
    "86956951692C1455416928552"
    "C545545456C54555545444556"
)

graph = []
for i in range(len(config)):
    cell = Cell(config[i], (i % MAZE_SIZE, i // MAZE_SIZE))
    graph.append(cell)

start = (1, 1)
end = (19, 14)

queue = []
queue.append(get_cell_at_pos(graph, start))

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

    print([x.position for x in path_cells])
    pathway = parse_path(path_cells)
    print(pathway)

else:
    print("Didnt find finish")

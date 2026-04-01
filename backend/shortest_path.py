MAZE_SIZE = 25

class Cell:
    def __init__(self, value, position):
        self.value = value
        self.position = position
        self.distance = 0
        self.caller = None
        self.is_visited = False

    def add_to_queue(self, caller):
        self.caller = caller
        self.distance = caller.distance + 1

    def north(self, graph):
        if self.value % 2:
            return get_cell_at_pos(graph, (self.position[0], self.position[1] - 1))
        else:
            return None


def get_available_neighbours(graph, queue, cell):
    res = {}

    north = cell.north(graph)
    if north != None and not north.is_visited:
        res.add(north)
    # and the same with others

# def make_step(graph, queue, current_pos):
#     next_cell = get_cell_at_pos(graph, (current_pos[0] + 1, current_pos[1]))

#     queue.append(graph[])


def get_cell_at_pos(graph, pos):
    i = pos.y * MAZE_SIZE + pos.x
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
for i in config:
    cell = Cell(config[i], (i % MAZE_SIZE, i // MAZE_SIZE))
    graph.append(cell)

start = (1, 1)
end = (19, 14)

current_pos = start
queue = []
queue.append(get_cell_at_pos(graph, start))





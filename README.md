*This project has been created as part of the 42 curriculum by dsalwa and stitov*

# A-Maze-ing

## Description

A-Maze-ing is a Python-based maze generator that creates random mazes based on a configuration file. The project demonstrates the use of algorithms, and structured data representation.

The program supports generating both standard and *perfect* mazes (with exactly one path between entry and exit), exporting them in a compact hexadecimal format, and displaying them visually.

---

## Instructions

### Requirements

* Python 3.10+
* pip (or equivalent package manager)

### Installation

```bash
make install
```

### Run

```bash
make run
```

or directly:

```bash
python3 a_maze_ing.py config.txt
```

---

## Configuration File Format

The program uses a `.txt` configuration file.

### Required fields:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Optional fields:

```
SEED=42
```

### Notes:

* Lines starting with `#` are ignored.
* ENTRY and EXIT must be inside maze bounds.
* ENTRY and EXIT must be different.

---

## Maze Generation Algorithm

### Chosen Algorithm: Recurisve Backtracker (DFS)

The maze is generated using a depth-first search (DFS) approach:

1. Start from a random cell.
2. Visit unvisited neighbors randomly.
3. Remove walls between current and next cell.
4. Backtrack when no unvisited neighbors remain.

### Why this algorithm?

* Simple to implement
* Produces perfect mazes naturally
* Efficient (O(N))

---

## Output File Format

Each cell is encoded as a hexadecimal digit representing walls:

| Bit | Direction |
| --- | --------- |
| 0   | North     |
| 1   | East      |
| 2   | South     |
| 3   | West      |

Example:

* `A (1010)` → East and West walls closed

## Reusable Module

The core logic is implemented in a reusable module:

### Class:

```
MazeGenerator
```

### Features:

* Based on config.txt file it creates a maze starting params
* You can generate a maze using render_maze function
* You can push maze settings to output_maze.txt using render_to_file function
* You can display directly in the console maze settings

### Example usage:

```python
from MazeGenerator import MazeGenerator

maze_generator = MazeGenerator()

maze_generator.render_to_file()
maze_generator.display_maze_settings()
maze_generator.render_maze()

```

---

---


### Algorithms

* Recursive Backtracker (DFS)
* Breadth-First Search (shortest path)

### AI Usage

AI was used for:

* understanding maze generation algorithms
* structuring the project

All generated content was reviewed, tested, and fully understood before use.

---

## Team & Project Management

### Roles

* dsalwa – backend part, code structure, work organizing
* stitov – frontend part, design, testing

---

## Additional Notes

* The maze guarantees full connectivity.
* Perfect mode ensures a single path between entry and exit.
* The “42” pattern is included when maze size allows it.

---

"""It is useful for debugging only"""
from mazegen.backend.maze_types import Cell


def display_wall_to_destroy(wall_to_destroy: int):
    print(f"Wall to destroy: {wall_to_destroy}")


def display_position(x: int, y: int) -> None:
    print(f"Current position: (x: {x}, y: {y})")


def display_wall(cell: Cell) -> None:
    print(f"Wall: {cell.walls} -> HEX: {hex(cell.walls)[2:]}")


def maze_direction_details(
    direction: str,
    go_or_back: int,
    x: int,
    y: int,
    count: int
) -> None:
    print(f"Count: {count}")
    print(f"Direction: {go_or_back} {direction}")
    print(f"Next position: (x: {x}, y: {y})")


def show_wall_after_changes(cell: Cell, picked_wall: int, x: int, y: int):

    print(f"\nPicked wall: {picked_wall}")

    print(f"Cell localisation: ({x}, {y})")
    print(cell)
    print()

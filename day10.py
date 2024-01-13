from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generator

INPUT1 = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""
EXPECTED1 = 4

INPUT2 = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
EXPECTED2 = 8


def test_case1():
    """Test case example 1 part 1"""
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """Test case example 2 part 1"""
    assert compute(INPUT2) == EXPECTED2


class Offsets(Enum):
    """
    Offsets in coords to go a direction in the grid.

    (delta_row, delta_col)
    """

    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


@dataclass
class Node:
    """Representation of a node in the grid"""

    symbol: str
    row: int
    col: int

    @property
    def is_start(self) -> bool:
        """Check if this node is the start node"""
        return self.symbol == "S"

    @property
    def neighbours(self) -> list[tuple[int, int]]:
        """Return a list of coordinates of neighbouring nodes"""
        match self.symbol:
            case "S":
                offsets = [
                    Offsets.NORTH.value,
                    Offsets.EAST.value,
                    Offsets.SOUTH.value,
                    Offsets.WEST.value,
                ]
            case ".":
                offsets = []
            case "|":
                offsets = [Offsets.NORTH.value, Offsets.SOUTH.value]
            case "-":
                offsets = [Offsets.WEST.value, Offsets.EAST.value]
            case "L":
                offsets = [Offsets.NORTH.value, Offsets.EAST.value]
            case "J":
                offsets = [Offsets.NORTH.value, Offsets.WEST.value]
            case "7":
                offsets = [Offsets.WEST.value, Offsets.SOUTH.value]
            case "F":
                offsets = [Offsets.EAST.value, Offsets.SOUTH.value]
            case _:
                raise ValueError(f"Invalid sumbol '{self.symbol}'.")
        return [(self.row + r, self.col + c) for (r, c) in offsets]

    def is_valid_neighbour(self, node: Node) -> bool:
        """Check if this node is a valid neighbour of the other node"""
        return (node.row, node.col) in self.neighbours


@dataclass
class Grid:
    grid: list[list[Node]]

    def get_start_of_maze(self) -> Node:
        """Return the start node of the maze"""
        for row in self.grid:
            for node in row:
                if node.is_start:
                    return node

        raise ValueError("No start node found in grid")

    def get_node_neighbours(self, node: Node) -> Generator[Node, None, None]:
        """Returns a list of nodes neigbouring the given node"""
        for rown, coln in node.neighbours:
            try:
                new_node = self.grid[rown][coln]

                if new_node.is_valid_neighbour(node):
                    yield new_node
            except IndexError:
                continue


def get_maze(grid: Grid) -> list[Node]:
    """Construct the maze for a given grid."""
    maze = []

    current_node = grid.get_start_of_maze()
    # previous node is needed for pathing.
    # initially we set it to the start node
    prev_node = current_node

    end_of_maze = False

    while not end_of_maze:
        maze.append(current_node)

        neighbours = [
            n
            for n in grid.get_node_neighbours(current_node)
            # Find neighbouring nodes that are not the previously visited node
            # And that is not the start node.s
            if n != prev_node and not n.is_start
        ]

        if not neighbours:
            # If we can't find any new valid neighbours, it means we are at the
            # end of the maze
            end_of_maze = True
        else:
            # Else continue with the next node
            prev_node = current_node
            current_node = neighbours[0]

    return maze


def compute(data: str) -> int:
    """Compute the result for part 1"""
    g = [
        [Node(c, rown, coln) for (coln, c) in enumerate(line)]
        for (rown, line) in enumerate(data.splitlines())
    ]

    grid = Grid(g)
    maze = get_maze(grid)

    return len(maze) // 2


def main() -> None:
    """Runnning puzzle input"""
    with open("day10_input.txt", "r") as f:
        data = f.read()

    result = compute(data)

    print(f"{result}")


if __name__ == "__main__":
    main()

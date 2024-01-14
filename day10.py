from __future__ import annotations

import functools
from dataclasses import dataclass
from enum import Enum
from typing import Generator

import pytest

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

INPUT3 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""
EXPECTED3 = 4

INPUT4 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""
EXPECTED4 = 8

INPUT5 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

EXPECTED5 = 10


@pytest.mark.parametrize(
    "input, expected",
    [
        (INPUT1, EXPECTED1),
        (INPUT2, EXPECTED2),
    ],
)
def test_case_part1(input, expected):
    """Test case example 1 part 1"""
    assert compute(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (INPUT3, EXPECTED3),
        (INPUT4, EXPECTED4),
        (INPUT5, EXPECTED5),
    ],
)
def test_case_part2(input, expected):
    """Test case example 2 part 1"""
    assert compute2(input) == expected


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

    row: int
    col: int
    symbol: str = "."

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


@dataclass
class Maze:
    nodes: list[Node]

    @staticmethod
    def _min_node(this: Node, that: Node) -> Node:
        """Return a node object that has the minimum coords of both nodes"""
        return Node(min(this.row, that.row), min(this.col, that.col))

    @staticmethod
    def _max_node(this: Node, that: Node) -> Node:
        """Return a node object that has the maximum coords of both nodes"""
        return Node(max(this.row, that.row), max(this.col, that.col))

    @functools.cached_property
    def bounding_box(self) -> tuple[int, int, int, int]:
        """Determine the bounding box of maze polygon"""

        min_node = functools.reduce(self._min_node, self.nodes)
        max_node = functools.reduce(self._max_node, self.nodes)
        return (min_node.row, max_node.row, min_node.col, max_node.col)

    @functools.cached_property
    def vertices(self) -> list[Node]:
        """
        Get the vertices of the maze.

        Remove the nodes where the direction doesn't change.
        i.e. vertical and horizontal nodes
        """
        return [n for n in self.nodes if n.symbol not in "|-"]

    def _find_convex_hull_node(self) -> Node:
        """
        Find a Node on the convex hull of the polygon (outside).

        Find the Node on the polygon that has the minimum column.
        If multiple nodes, select the ones with the smalles row.
        """
        _, _, col_min, _ = self.bounding_box

        # Find all nodes that lie in the min X position
        nodes = [node for node in self.nodes if node.col == col_min]

        if len(nodes) > 1:
            # If multiple nodes, find one with lowest row value
            row_min = min(node.row for node in nodes)
            nodes = [node for node in nodes if node.row == row_min]

        return nodes[0]

    @property
    def positive_orientation(self) -> bool:
        """
        Check that the node order of the maze is a positive orientation.
        Use logic defined here:
        https://en.wikipedia.org/wiki/Curve_orientation#Orientation_of_a_simple_polygon
        """
        node = self._find_convex_hull_node()

        idx = self.vertices.index(node)
        n_a = self.vertices[(idx - 1) % len(self.vertices)]
        n_b = self.vertices[idx]
        n_c = self.vertices[(idx + 1) % len(self.vertices)]

        return (
            (n_b.col * n_c.row + n_a.col * n_b.row + n_a.row * n_c.col)
            - (n_a.row * n_b.col + n_b.row * n_c.col + n_a.col * n_c.row)
        ) > 0


@dataclass
class Vertex:
    n1: Node
    n2: Node

    @property
    def direction(self):
        if self.n1.col == self.n2.col:
            return "V"
        else:
            return "H"


def get_maze(grid: Grid) -> Maze:
    """Construct the maze for a given grid."""
    nodes = []

    current_node = grid.get_start_of_maze()
    # previous node is needed for pathing.
    # initially we set it to the start node
    prev_node = current_node

    end_of_maze = False

    while not end_of_maze:
        nodes.append(current_node)

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

    maze = Maze(nodes)

    # Check maze orientation
    if not maze.positive_orientation:
        # Ensure maze in positive orientation
        nodes.reverse()
        maze = Maze(nodes)

    return Maze(nodes)


def compute_area_in_maze(maze: Maze) -> int:
    """
    Compute the are enclosed by the maze polygon using shoelace formula:
    https://en.wikipedia.org/wiki/Shoelace_formula
    """
    area = 0
    for idx in range(len(maze.vertices)):
        n1 = maze.vertices[idx]
        n2 = maze.vertices[(idx + 1) % len(maze.vertices)]
        area += (n1.row + n2.row) * (n1.col - n2.col)

    return area // 2


def pick_theorem(maze: Maze, area: int) -> int:
    """
    Using the pick theorem too calculate how many nodes are included inside the
    maze polygon:
    https://en.wikipedia.org/wiki/Pick%27s_theorem
    """
    return area + 1 - len(maze.nodes) // 2


def compute(data: str) -> int:
    """Compute the result for part 1"""
    g = [
        [Node(rown, coln, c) for (coln, c) in enumerate(line)]
        for (rown, line) in enumerate(data.splitlines())
    ]

    grid = Grid(g)
    maze = get_maze(grid)

    return len(maze.nodes) // 2


def compute2(data: str) -> int:
    """Compute the result for part 2"""
    g = [
        [Node(rown, coln, c) for (coln, c) in enumerate(line)]
        for (rown, line) in enumerate(data.splitlines())
    ]

    grid = Grid(g)
    maze = get_maze(grid)

    area = compute_area_in_maze(maze)

    return pick_theorem(maze, area)


def main() -> None:
    """Runnning puzzle input"""
    with open("day10_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    result2 = compute2(data)
    print(f"{result=}")
    print(f"{result2=}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import math
from dataclasses import dataclass
from dataclasses import field
from itertools import count
from typing import Generator

import pytest

from utils import Offsets

INPUT1 = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

EXPECTED1 = 374


def test_case1():
    """Test example part 1"""
    assert compute(INPUT1) == EXPECTED1


@pytest.mark.parametrize("multiplier, expected", [(10, 1030), (100, 8410)])
def test_case2(multiplier, expected):
    assert compute(INPUT1, multiplier) == expected


@dataclass
class Grid:
    grid: list[list[Node]]

    @property
    def size(self) -> tuple[int, int]:
        return (len(self.grid), len(self.grid[0]))

    def get_galaxy_nodes(self):
        return [node for row in self.grid for node in row if node.is_galaxy]

    def get_neighbours(self, node: Node) -> Generator[Node, None, None]:
        nrow, ncol = self.size
        for offset in Offsets:
            new_row = node.row + offset.value[0]
            new_col = node.col + offset.value[1]

            if new_row < 0 or new_col < 0 or new_row >= nrow or new_col >= ncol:
                continue

            yield self.grid[new_row][new_col]

    def get_cost_grid(self, mult: int) -> list[list[int]]:
        """Construct a grid with the cost to cross each cell."""
        return [[mult if c.symbol == "X" else 1 for c in row] for row in self.grid]


@dataclass(order=True)
class Node:
    row: int
    col: int
    symbol: str = "."
    # This is an automatic counter used as an ID field
    id: int = field(default_factory=count().__next__)

    @property
    def is_galaxy(self) -> bool:
        """Return True of Node is `#`."""
        return self.symbol == "#"

    @property
    def is_empty(self) -> bool:
        """Return True of Node is `.`."""
        return self.symbol in ".X"

    def distance(self, other: Node) -> float:
        """Get the euclidian distance between 2 Nodes."""
        return math.sqrt((self.row - other.row) ** 2 + (self.col - other.col) ** 2)


def get_combinations(
    galaxies: list[Node],
) -> Generator[tuple[Node, Node], None, None]:
    """Creates a generator with all combinations of galaxies of length 2."""
    for i in range(len(galaxies) - 1):
        for j in range(i + 1, len(galaxies)):
            yield (galaxies[i], galaxies[j])


def expand_empty(data: list[list[str]]) -> list[list[str]]:
    """
    When entire row/column is empty, replace it with `X`.
    This still counts as empty, but when calculating the cost matrix,
    X-values get multiplied by the giver multiplier.
    """
    empty_row = ["X"] * len(data[0])
    empty_rows = [idx for idx, row in enumerate(data) if all(c in ".X" for c in row)]

    empty_cols = [
        idx for idx in range(len(data[0])) if all(row[idx] in ".X" for row in data)
    ]

    for idx in empty_rows:
        data[idx] = empty_row.copy()
    for ridx in range(len(data)):
        for cidx in empty_cols:
            data[ridx][cidx] = "X"

    return data


def parse_grid(data: str, expand: bool = True) -> Grid:
    """
    Parse the grid from the given input string.
    Optionally expand empty rows/columns in input string.
    """
    # get list of list of characters
    g = [[c for c in line] for line in data.splitlines()]

    if expand:
        g = expand_empty(g)

    nodes = [
        [Node(ridx, cidx, c) for (cidx, c) in enumerate(row)]
        for ridx, row in enumerate(g)
    ]
    return Grid(nodes)


def get_gridpoints_between_nodes(
    n1: Node, n2: Node
) -> Generator[tuple[int, int], None, None]:
    """
    Create a list of coordinates to travel from 1 node to another.
    A simple L-shaped movement is assumed.
    """
    min_row = min(n1.row, n2.row)
    max_row = max(n1.row, n2.row)
    min_col = min(n1.col, n2.col)
    max_col = max(n1.col, n2.col)

    for colidx in range(min_col, max_col + 1):
        yield (min_row, colidx)

    for rowidx in range(min_row + 1, max_row + 1):
        yield (rowidx, min_col)


def compute(data: str, multiplier: int = 2) -> int:
    """Compute the result for part 2"""
    grid = parse_grid(data)
    galaxies = grid.get_galaxy_nodes()

    # Calculate the cost grid for traveling across space
    cost_grid = grid.get_cost_grid(multiplier)

    total_length = 0
    for start, stop in get_combinations(galaxies):
        # get simple path for travelling from 1 node to other
        coords = get_gridpoints_between_nodes(start, stop)

        # Calculate path length
        # subtract 1 because we don't need the cost of the start_node
        path_length = sum(cost_grid[row][col] for row, col in coords) - 1
        total_length += path_length

    return total_length


def main() -> None:
    """Runnning puzzle input"""
    with open("day11_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    result2 = compute(data, 1000000)
    print(f"{result=}")
    print(f"{result2=}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import math
from dataclasses import dataclass, field
from itertools import count
from typing import Generator

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
        return self.symbol == "."

    def distance(self, other: Node) -> float:
        """Get the euclidian distance between 2 Nodes."""
        return math.sqrt((self.row - other.row) ** 2 + (self.col - other.col) ** 2)


def get_galaxy_combinations(
    galaxies: list[Node],
) -> Generator[tuple[Node, Node], None, None]:
    """Creates a generator with all combinations of galaxies of length 2."""
    for i in range(len(galaxies) - 1):
        for j in range(i + 1, len(galaxies)):
            yield (galaxies[i], galaxies[j])


def expand_empty(data: list[list[str]]) -> list[list[str]]:
    """
    Expands empty columns/rows in the data.
    If entire row/col is empty (i.e. `.`), add another empty row/col
    right next to it.
    """
    empty_row = ["."] * len(data[0])
    empty_rows = [idx for idx, row in enumerate(data) if all(c == "." for c in row)]
    empty_rows.reverse()

    empty_cols = [
        idx for idx in range(len(data[0])) if all(row[idx] == "." for row in data)
    ]
    empty_cols.reverse()

    for idx in empty_rows:
        data[idx:idx] = [empty_row]

    for ridx in range(len(data)):
        for cidx in empty_cols:
            data[ridx][cidx:cidx] = ["."]

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


def compute(data: str) -> int:
    """Compute the result for part 1"""
    grid = parse_grid(data)
    galaxies = grid.get_galaxy_nodes()

    total_length = 0
    for start, stop in get_galaxy_combinations(galaxies):
        # length of parths is just the sum of delta_row + delta_column
        n_steps = abs(stop.row - start.row) + abs(stop.col - start.col)
        total_length += n_steps

    return total_length


def main() -> None:
    """Runnning puzzle input"""
    with open("day11_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    print(f"{result=}")


if __name__ == "__main__":
    main()

import heapq
from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Tuple

from utils import Offsets

INPUT1 = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""
EXPECTED1 = 94


@dataclass(frozen=True, eq=True, order=True)
class Node:
    x: int
    y: int
    symbol: str
    is_start: bool = False
    is_end: bool = False

    @property
    def is_path(self) -> bool:
        return self.symbol == "."

    @property
    def is_forest(self) -> bool:
        return self.symbol == "#"

    @property
    def is_slope(self) -> bool:
        return self.symbol in (">", "<", "v", "^")

    @property
    def is_walkable(self) -> bool:
        return self.is_path or self.is_slope

    def get_neighbour_coords(self) -> List[Tuple[int, int]]:
        """
        Returns a list of coordinates for the neighbour nodes
        that can be visited from this node.
        """
        if self.is_forest:
            return []

        # In a slope can only move in that direction
        if self.is_slope:
            match self.symbol:
                case ">":
                    return [(self.x + 1, self.y)]
                case "<":
                    return [(self.x - 1, self.y)]
                case "^":
                    # top row is idx 0
                    return [(self.x, self.y - 1)]
                case "v":
                    return [(self.x, self.y + 1)]
                case _:
                    raise ValueError(
                        f"Got an unknown symbol '{self.symbol}' for slope."
                    )

        return [(self.x + off.value[1], self.y + off.value[0]) for off in Offsets]


class Grid:
    def __init__(self, raw_grid: str):
        self.raw_grid = raw_grid
        self.grid = self._parse_grid(raw_grid)
        self._start_pos: Optional[Tuple[int, int]] = None
        self._end_pos: Optional[Tuple[int, int]] = None
        self.nrows = len(self.grid)
        self.ncols = len(self.grid[0])

        self._find_end_pos()
        self._find_start_pos()

    def _parse_grid(self, data: str) -> List[List[Node]]:
        grid = []
        for row_idx, line in enumerate(data.splitlines()):
            row = []
            for col_idx, symbol in enumerate(line):
                row.append(Node(col_idx, row_idx, symbol))

            grid.append(row)

        return grid

    def _find_start_pos(self) -> Tuple[int, int]:
        """
        Look in the first row and find the path node
        """
        node = [x for x in self.grid[0] if x.is_path]

        # If multiple start nodes found, something went wrong
        assert len(node) == 1

        # Update grid with start node marked
        start_node = Node(node[0].x, node[0].y, node[0].symbol, is_start=True)
        self.grid[start_node.y][start_node.x] = start_node

        return (node[0].x, node[0].y)

    def _find_end_pos(self) -> Tuple[int, int]:
        """
        Look in the last row and find the path node
        """
        node = [x for x in self.grid[-1] if x.is_path]

        # If multiple start nodes found, something went wrong
        assert len(node) == 1

        # Update grid with start node marked
        end_node = Node(node[0].x, node[0].y, node[0].symbol, is_end=True)
        self.grid[end_node.y][end_node.x] = end_node

        return (end_node.x, end_node.y)

    def get_node(self, x: int, y: int) -> Optional[Node]:
        """
        Return the node at grid coordinates (x, y)
        """
        if self.in_grid(x, y):
            return self.grid[y][x]

        return None

    @property
    def start_pos(self) -> Tuple[int, int]:
        """
        Return the grid coordinates of the starting node.

        If still unknown determine start node
        """
        if self._start_pos is None:
            self._start_pos = self._find_start_pos()

        return self._start_pos

    @property
    def end_pos(self) -> Tuple[int, int]:
        """
        Return the grid coordinates of the enfing node.

        If still unknown determine end node
        """
        if self._end_pos is None:
            self._end_pos = self._find_end_pos()

        return self._end_pos

    def in_grid(self, x: int, y: int) -> bool:
        """
        Returns True if the selected coordinates are within the grid.
        """
        return 0 <= x < self.ncols and 0 <= y < self.nrows

    def find_longest_path(self) -> int:
        """
        BFS approach to find all paths to the end node and return the number of steps
        taken in the longest path.

        This works, but is very slow...
        Probably cause by reprocessing similar paths multiple times.
        """
        paths2end = []
        start_node = self.get_node(self.start_pos[0], self.start_pos[1])

        assert start_node is not None

        queue: List[List[Node]] = []
        heapq.heappush(queue, [start_node])

        while queue:
            qpath = heapq.heappop(queue)

            if qpath[-1].is_end:
                paths2end.append(qpath)
                continue

            for nx, ny in qpath[-1].get_neighbour_coords():
                nnode = self.get_node(nx, ny)

                if nnode is None:
                    continue

                if nnode in qpath:
                    continue

                if not nnode.is_walkable:
                    continue

                new_path = qpath + [nnode]
                heapq.heappush(queue, new_path)

        return max(len(path) - 1 for path in paths2end)


def test_case1():
    assert compute(INPUT1) == EXPECTED1


def compute(data: str) -> int:
    grid = Grid(data)
    return grid.find_longest_path()


def main():
    """Run puzzle input"""
    with open("day23_input.txt", "r") as f:
        data = f.read()

    result = compute(data)

    print(f"{result=}")


if __name__ == "__main__":
    main()

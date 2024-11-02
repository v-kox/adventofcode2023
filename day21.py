from collections import deque
from typing import Iterable
from typing import Optional

from utils import Offsets

INPUT1 = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""
EXPECTED1 = 16


def test_case1():
    """Test case for example part 1"""
    assert compute(INPUT1, 6) == EXPECTED1


class Node:
    """Representation of a Node"""

    def __init__(self, row: int, col: int, symbol: str = "") -> None:
        self.row = row
        self.col = col
        self.symbol = symbol

    def __repr__(self) -> str:
        return f"Node({self.row}, {self.col}, '{self.symbol}')"

    @property
    def is_rock(self) -> bool:
        """Return True if this node is a rock node"""
        return self.symbol == "#"

    @property
    def is_start(self) -> bool:
        """Return True if this is the start node"""
        return self.symbol == "S"


class Grid:
    """Representation of the grid"""

    def __init__(self, grid: list[list[Node]]):
        self.grid = grid
        self._start_node: Optional[Node] = None

    @property
    def nrows(self) -> int:
        """Returns the number of rows from the grid"""
        return len(self.grid)

    @property
    def ncols(self) -> int:
        """Returns the number of columns from the grid"""
        return len(self.grid[0])

    def in_grid(self, node: Node) -> bool:
        """Return True if the coordinates of the node are within the grid"""
        return 0 <= node.row < self.nrows and 0 <= node.col < self.ncols

    def coord_in_grid(self, rown: int, coln: int) -> bool:
        """Return True if the coordinates are within the grid"""
        return 0 <= rown < self.nrows and 0 <= coln < self.ncols

    @property
    def start_node(self) -> Node:
        """Return the start_node of the grid. Or find it if it is no known yet."""
        if self._start_node is not None:
            return self._start_node
        else:
            for row in self.grid:
                for node in row:
                    if node.is_start:
                        self._start_node = node
                        return node
        raise AssertionError("Could not find start node")

    def get_ascii_grid(self, nodes: Optional[Iterable[Node]] = None) -> str:
        """
        Get printable version of the grid
        Possible with list of nodes indicated
        """
        raw_grid = [[node.symbol for node in line] for line in self.grid]

        if nodes:
            for node in nodes:
                raw_grid[node.row][node.col] = "O"

        return "\n".join("|".join(line) for line in raw_grid)

    def get_neighbours(self, node: Node) -> list[Node]:
        """
        return a list of neighbour nodes for the given nodes
        step count of returned nodes is 1 higher than input node
        """
        nodes = []
        for offset in Offsets:
            new_row = node.row + offset.value[0]
            new_col = node.col + offset.value[1]

            if self.coord_in_grid(new_row, new_col):
                nnode = self.grid[new_row][new_col]
                nodes.append(nnode)

        return nodes


def parse_grid(data: str) -> Grid:
    """Parse string data into grid"""
    return Grid(
        [
            [Node(row_idx, col_idx, node) for col_idx, node in enumerate(line)]
            for row_idx, line in enumerate(data.strip().splitlines())
        ]
    )


def bfs_grid(grid: Grid, start: Node) -> dict[Node, int]:
    """
    This is a bread first search implementation to find the minimum number of steps
    needed to reach any point in a grid from a given start point `start`
    """
    visited: dict[Node, int] = {}

    queue: deque[tuple[int, Node]] = deque([(0, start)])
    while queue:
        dist, node = queue.popleft()

        if node in visited:
            # node already checked. Skip.
            continue

        visited[node] = dist

        neighbours = grid.get_neighbours(node)

        for neighbour in neighbours:
            if not neighbour.is_rock:
                queue.append((dist + 1, neighbour))

    return visited


def is_even(i: int) -> bool:
    return i % 2 == 0


def is_odd(i: int) -> bool:
    return i % 2 > 0


def compute(data: str, max_steps: int) -> int:
    """Compute the result of the provided input for the max_steps"""
    grid = parse_grid(data)
    start_node = grid.start_node

    # Get minimum distance to each reachable node
    bfsgrid = bfs_grid(grid, start_node)

    # if the max_steps is even, the minimal distance to reach it must also be even.
    # since walkbacks are allowed.
    if max_steps % 2 == 0:
        f = is_even
    else:
        f = is_odd

    # filter out irrelivant nodes
    possible_nodes = [(n, d) for n, d in bfsgrid.items() if d <= max_steps and f(d)]

    return len(possible_nodes)


def compute2(data: str, max_steps: int) -> int:
    """
    Compute part 2 the result of the provided input for the max_steps.

    Solution is taken from:
    https://advent-of-code.xavd.id/writeups/2023/day/21/

    Really specific for the input data. But the end result is correct
    """
    grid = parse_grid(data)
    start_node = grid.start_node

    # square grid is assumed
    dist2edge = grid.ncols // 2

    # Get minimum distance to each reachable node
    bfsgrid = bfs_grid(grid, start_node)

    # get total number of even and odd nodes in the map
    n_even_nodes = sum(1 for (_, dist) in bfsgrid.items() if dist % 2 == 0)
    n_odd_nodes = sum(1 for (_, dist) in bfsgrid.items() if dist % 2 == 1)

    # get number of even/odd nodes you can reach in less than dist2edge steps
    n_even_reachable = sum(
        dist <= dist2edge for (_, dist) in bfsgrid.items() if dist % 2 == 0
    )
    n_odd_reachable = sum(
        dist <= dist2edge for (_, dist) in bfsgrid.items() if dist % 2 == 1
    )

    # get number of even/odd nodes we cannot reach in less than dist2edge steps
    n_even_corners = sum(
        dist > dist2edge for (_, dist) in bfsgrid.items() if dist % 2 == 0
    )
    n_odd_corners = sum(
        dist > dist2edge for (_, dist) in bfsgrid.items() if dist % 2 == 1
    )

    # number of tile boundaries we will cross.
    # Assuming we start in the center
    n_tile_boundaries = (max_steps - dist2edge) // grid.ncols

    if max_steps % 2 == 1:
        n_odd_tiles = (n_tile_boundaries + 1) ** 2
        n_even_tiles = n_tile_boundaries**2
    else:
        n_odd_tiles = n_tile_boundaries**2
        n_even_tiles = (n_tile_boundaries + 1) ** 2

    return (
        n_odd_tiles * n_odd_nodes
        + n_even_tiles * n_even_nodes
        - ((n_tile_boundaries + 1) * n_odd_corners)
        + (n_tile_boundaries * n_even_corners)
    )


def main():
    """Run puzzle input"""
    with open("day21_input.txt", "r") as f:
        data = f.read()

    result = compute(data, 64)
    result2 = compute2(data, 26501365)

    print(f"{result=}")
    print(f"{result2=}")


if __name__ == "__main__":
    main()

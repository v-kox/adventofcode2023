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

    def __init__(self, row: int, col: int, symbol: str = "", n_steps: int = 0) -> None:
        self.row = row
        self.col = col
        self.symbol = symbol
        self.n_steps = n_steps

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

            if self.in_grid(Node(new_row, new_col, "")):
                nnode = self.grid[new_row][new_col]
                nnode.n_steps = node.n_steps + 1
                nodes.append(nnode)

        return nodes


def walk_grid(grid: Grid, max_steps: int) -> set[Node]:
    """
    Walk the grid and determine which nodes you can reach in exactly
    `max_steps` number of steps.
    """
    start_node = grid.start_node
    walk_nodes: set[Node] = set()

    # queue of nodes to process
    queue = [start_node]

    # Set of coordinates of already visited nodes.
    visited: set[tuple[int, int]] = set()

    while queue:
        node = queue.pop(0)

        # If nodes already visited skip it.
        # Otherwise add it to visited set and continue
        if (node.row, node.col) in visited:
            continue
        else:
            visited.add((node.row, node.col))

        # If node is a rock, we cant pass so continue
        if node.is_rock:
            continue

        # if we exceed the max number of steps we can't reach it, so continue
        if node.n_steps > max_steps:
            continue

        # If the total number of remaining steps ,after we reach the current node,
        # is divisible by 2, then we can reach this node as an end point by walking to
        # the next node and back until we are out of steps.
        # This avoids reprocessing nodes many times with different step counts
        if (max_steps - node.n_steps) % 2 == 0:
            walk_nodes.add(node)

        # Get neighbours of the current node.
        # If they are not yet visited, add them to queue
        neighbours = grid.get_neighbours(node)
        queue += [n for n in neighbours if (n.row, n.col) not in visited]

    # Return reachable nodes
    return walk_nodes


def parse_grid(data: str) -> Grid:
    """Parse string data into grid"""
    return Grid(
        [
            [Node(row_idx, col_idx, node) for col_idx, node in enumerate(line)]
            for row_idx, line in enumerate(data.strip().splitlines())
        ]
    )


def compute(data: str, max_steps: int) -> int:
    """Compute the result of the provided input for the max_steps"""
    grid = parse_grid(data)
    reachable_nodes = walk_grid(grid, max_steps)

    return len(reachable_nodes)


def main():
    """Run puzzle input"""
    with open("day21_input.txt", "r") as f:
        data = f.read()

    result = compute(data, 64)

    print(f"{result=}")


if __name__ == "__main__":
    main()

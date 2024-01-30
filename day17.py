from __future__ import annotations

import heapq
import math
from typing import Generator, NamedTuple

from utils import Offsets

INPUT1 = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
EXPECTED1 = 102


def test_case1():
    assert compute(INPUT1) == EXPECTED1


# Some type aliases
Coord = tuple[int, int]
Direction = tuple[int, int]
Steps = int
NodeId = tuple[Coord, Direction, Steps]


class Node(NamedTuple):
    """Wrapper class to represent a Node in the path"""

    row: int
    col: int
    cost: int
    direction: Offsets
    steps: int

    def same_loc(self, other: Node) -> bool:
        return self.coord == other.coord

    @property
    def coord(self) -> Coord:
        return (self.row, self.col)

    @property
    def id(self) -> NodeId:
        """Create an ID to be used in Dijkstra alghoritm"""
        return (self.coord, self.direction.value, self.steps)

    @property
    def symbol(self) -> str:
        """Set a symbol for printing the Node"""
        match self.direction:
            case None:
                return "O"
            case Offsets.NORTH:
                return "^"
            case Offsets.EAST:
                return ">"
            case Offsets.SOUTH:
                return "v"
            case Offsets.WEST:
                return "<"


class Grid(NamedTuple):
    """Wrapper class to represent the grid"""

    cost: list[list[int]]

    @property
    def nrows(self) -> int:
        return len(self.cost)

    @property
    def ncols(self) -> int:
        return len(self.cost[0])

    def get_cost(self, row: int, col: int) -> int:
        """Get the cost to enter a specific coordinate in the grid"""
        if row < 0 or row >= self.nrows or col < 0 or col >= self.ncols:
            raise ValueError("Outside of grid range")

        return self.cost[row][col]

    def get_next_node(self, node: Node, direction: Offsets) -> Node:
        """
        Get the next node when moving from the given node into a given direction.
        Raises a ValueError if the new Node lies outside of the Grid.
        """
        new_row = node.row + direction.value[0]
        new_col = node.col + direction.value[1]

        if new_row < 0 or new_row >= self.nrows or new_col < 0 or new_col >= self.ncols:
            raise ValueError("Outside of grid range")

        steps = node.steps + 1 if direction == node.direction else 1
        cost = self.cost[new_row][new_col]

        return Node(new_row, new_col, cost, direction, steps)

    def get_coords(self) -> Generator[Coord, None, None]:
        """Generator to loop over all coordinates in the Grid"""
        for row in range(self.nrows):
            for col in range(self.ncols):
                yield (row, col)

    def print_path(self, path: list[Node], show_cost: bool = False) -> None:
        """
        Helper function to print a Path on the grid
        """
        raw_grid = [[f"{c}" if show_cost else "." for c in line] for line in self.cost]

        for node in path:
            raw_grid[node.row][node.col] = node.symbol

        raw_str = "\n".join("|".join(line) for line in raw_grid)
        print(f"\n{raw_str}\n")


def get_path_dijkstra(grid: Grid, start: Node, end: Node) -> tuple[int, list[Node]]:
    """
    Implementation of Dijkstra's pathfinding alghoritm.
    https://en.wikipedia.org/wiki/Dijkstra's_algorithm
    """

    def get_path_to_node(node: Node) -> list[Node]:
        """
        Look back through the dictionary and return the path to the given node.
        """
        if node.id not in prev_nodes:
            return [node]

        return [node] + get_path_to_node(prev_nodes[node.id])

    # Dictionary containing the costs to read a certain Node.
    dist: dict[NodeId, int] = {}
    dist[start.id] = 0

    # Dictionary containing the node used to get to the key Node
    prev_nodes: dict[NodeId, Node] = {}

    # Set of expanded nodes
    visited: set[NodeId] = set()

    # Priority Queue to expand the nodes in the grid.
    queue: list[tuple[int, Node, int]] = []
    heapq.heappush(queue, (dist[start.id], start, 0))

    while queue:
        # Get the next Node in the queue and add it to the visited set
        ccost, cnode, csteps = heapq.heappop(queue)
        visited.add(cnode.id)

        if cnode.coord == end.coord:
            # If we are at the coordinates of the end node. We found the path.
            # Construct the path and return the cost to reach the end node.
            return ccost, get_path_to_node(cnode)

        # Loop over all possible directions
        for offset in Offsets:
            if offset == cnode.direction.reverse():
                # We cannot go in the reverse direction from which we are coming.
                # i.e. We went South to reach the current node. Then we can't go
                # North
                continue

            try:
                # Get the neighbour Node in the giver direction
                nnode = grid.get_next_node(cnode, offset)
            except ValueError:
                continue

            if nnode.id in visited:
                # If Node already visited, continue
                continue

            if nnode.steps > 3:
                # Cannot move more than 3 steps into any direction
                continue

            # Calculate the cost to reach the node.
            ncost = ccost + nnode.cost
            if ncost < dist.get(nnode.id, math.inf):
                # If the cost is less than the previously known cost,
                # Update the dist and prev_nodes dictionaries
                # and add the node to the queue
                dist[nnode.id] = ncost
                prev_nodes[nnode.id] = cnode
                heapq.heappush(queue, (ncost, nnode, nnode.steps))

    raise AssertionError("Cannot reach end node.")


def read_grid(data: str) -> Grid:
    grid = [[int(c) for c in line] for line in data.strip().splitlines()]
    return Grid(grid)


def compute(data: str) -> int:
    """Compute the result for the puzzle input"""
    grid = read_grid(data)

    # Get start and end nodes
    start = Node(0, 0, 0, Offsets.EAST, 0)
    max_row = grid.nrows - 1
    max_col = grid.ncols - 1
    end = Node(max_row, max_col, grid.get_cost(max_row, max_col), Offsets.EAST, 0)

    cost, path = get_path_dijkstra(grid, start, end)

    return cost


def main():
    """Run puzzle input"""
    with open("day17_input.txt", "r") as f:
        data = f.read()

    result = compute(data)

    print(f"{result=}")


if __name__ == "__main__":
    main()

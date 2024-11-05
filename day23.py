from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
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
EXPECTED2 = 154


def test_case1():
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    assert compute2(INPUT1) == EXPECTED2


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

    def get_neighbour_coords_no_slope(self) -> List[Tuple[int, int]]:
        """
        Returns a list of coordinates for the neighbour nodes
        that can be visited from this node.

        In this version slopes are ignored and just return all neighbours
        """
        if self.is_forest:
            return []

        return [(self.x + off.value[1], self.y + off.value[0]) for off in Offsets]


class Grid:
    def __init__(self, raw_grid: str):
        self.raw_grid = raw_grid
        self.grid = self._parse_grid(raw_grid)
        self._start_pos: Optional[Tuple[int, int]] = None
        self._end_pos: Optional[Tuple[int, int]] = None
        self.nrows = len(self.grid)
        self.ncols = len(self.grid[0])

        # make sure start and end points are initialized
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

    def _build_graph(self, *, ignore_slope: bool) -> Dict[Node, List[Tuple[int, Node]]]:
        """
        Builds a graph out of the grid.
        Returns a dict where the values are the child nodes and cost to get to child
        node
        """

        def _find_next_nodes(node: Node) -> List[Tuple[int, Node]]:
            """
            For the graph, child nodes are identified as nodes where the path splits up,
            dead ends or on the start and end positions.

            This drastically reduces the number of nodes in the final graph
            """
            neighbours: List[Tuple[int, Node]] = []
            queue: List[Tuple[int, Set[Node], Node]] = [(0, set(), node)]

            while queue:
                qdist, qvisited, qnode = queue.pop()

                if qnode.is_end:
                    neighbours.append((qdist, qnode))
                    continue

                # Depending on ignore_slope option, use different functions to get
                # neighbours.
                if ignore_slope:
                    ncoords = qnode.get_neighbour_coords_no_slope()
                else:
                    ncoords = qnode.get_neighbour_coords()
                nnodes = [self.get_node(x, y) for x, y in ncoords]

                # make sure neighbour nodes exist, are walkable and not
                # yet visited
                nodes = [
                    n
                    for n in nnodes
                    if n is not None and n.is_walkable and n not in qvisited
                ]

                # Split found after qnode, so add qnode to neighbour
                # Also check that qnode is not the node we originally started with
                if len(nodes) > 1 and qnode != node:
                    neighbours.append((qdist, qnode))
                    continue

                # if we are in a dead end, add node to neighbours and continue
                if len(nodes) == 0:
                    neighbours.append((qdist, qnode))
                    continue

                # add neighbour nodes to the queue until an end point is foud
                for nnode in nodes:
                    queue.append((qdist + 1, qvisited | {qnode}, nnode))

            return neighbours

        graph: Dict[Node, List[Tuple[int, Node]]] = {}
        queue = [self.get_start_node()]
        visited: Set[Node] = set()

        while queue:
            qnode = queue.pop()

            if qnode in visited:
                continue
            visited.add(qnode)

            for dist, node in _find_next_nodes(qnode):
                if qnode in graph:
                    graph[qnode].append((dist, node))
                else:
                    graph[qnode] = [(dist, node)]

                if node not in visited:
                    queue.append(node)

        return graph

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

    def get_start_node(self) -> Node:
        """
        Return the start node
        """
        start_node = self.get_node(self.start_pos[0], self.start_pos[1])
        assert start_node is not None

        return start_node

    def get_end_node(self) -> Node:
        """
        Return the end node
        """
        end_node = self.get_node(self.end_pos[0], self.end_pos[1])
        assert end_node is not None

        return end_node

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

    def find_longest_path(self, *, ignore_slope: bool) -> int:
        """
        Create graph from the maze and do breath first search search on the maze
        """
        longest_path = 0
        start_node = self.get_start_node()
        queue: List[Tuple[int, Set[Node], Node]] = [(0, set(), start_node)]
        graph = self._build_graph(ignore_slope=ignore_slope)

        while queue:
            qdist, qvisited, qnode = queue.pop()

            if qnode.is_end:
                if qdist > longest_path:
                    longest_path = qdist
                continue

            for ndist, nnode in graph[qnode]:
                if nnode not in qvisited:
                    queue.append((qdist + ndist, qvisited | {qnode}, nnode))

        return longest_path


def compute(data: str) -> int:
    """Compute result for part 1"""
    grid = Grid(data)
    return grid.find_longest_path(ignore_slope=False)


def compute2(data: str) -> int:
    """Compute result for part 2"""
    grid = Grid(data)
    return grid.find_longest_path(ignore_slope=True)


def main():
    """Run puzzle input"""
    with open("day23_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    print(f"{result=}")

    result2 = compute2(data)
    print(f"{result2=}")


if __name__ == "__main__":
    main()

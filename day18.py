import re
from typing import NamedTuple

from utils import Offsets

INPUT1 = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
EXPECTED1 = 62
EXPECTED2 = 952408144115


def test_case1():
    """test case part 1"""
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    assert compute2(INPUT1) == EXPECTED2


Coord = tuple[int, int]
Step = tuple[Offsets, int]


class Node(NamedTuple):
    """wrapper class for a Node"""

    row: int
    col: int

    @property
    def coord(self) -> Coord:
        return (self.row, self.col)


class Grid(NamedTuple):
    """wrapper class for a grid"""

    min_row: int
    max_row: int
    min_col: int
    max_col: int

    def print_path(self, path: list[Node]) -> None:
        raw_grid = [
            ["." for _ in range(self.min_col, self.max_col + 1)]
            for _ in range(self.min_row, self.max_row + 1)
        ]

        for node in path:
            raw_grid[node.row][node.col] = "#"

        raw_str = "\n".join(" ".join(line) for line in raw_grid)
        print(f"\n{raw_str}\n")


def compute_end_vertex(start: Node, direction: Offsets, steps: int) -> Node:
    """Compute the next node of the vertex"""
    new_row = start.row + steps * direction.value[0]
    new_col = start.col + steps * direction.value[1]

    return Node(new_row, new_col)


def parse_line(line: str) -> Step:
    """Get the data from a line of data"""
    re_line = re.compile(r"([A-Z]) (\d+) \(#[a-z0-9]{6}\)")

    re_match = re_line.match(line)

    if re_match is None:
        raise ValueError(f"Cannot properly parse line {line}.")

    dir_str, nsteps = re_match.groups()

    match dir_str:
        case "U":
            direction = Offsets.NORTH
        case "L":
            direction = Offsets.WEST
        case "D":
            direction = Offsets.SOUTH
        case "R":
            direction = Offsets.EAST
        case _:
            raise ValueError(f"Unknown direction string: {dir_str}")

    return (direction, int(nsteps))


def parse_line_color(line: str) -> Step:
    """Parse the step data from the color hex value in the line"""
    re_line = re.compile(r"[A-Z] \d+ \(#([a-z0-9]{5})(\d)\)")

    re_match = re_line.match(line)

    if re_match is None:
        raise ValueError(f"Cannot properly parse line {line}.")

    nsteps, dir_str = re_match.groups()

    match dir_str:
        case "0":
            direction = Offsets.EAST
        case "1":
            direction = Offsets.SOUTH
        case "2":
            direction = Offsets.WEST
        case "3":
            direction = Offsets.NORTH
        case _:
            raise ValueError(f"Unknown direction string: {dir_str}")
    # breakpoint()
    return (direction, int(nsteps, 16))


def compute_area(nodes: list[Node]) -> int:
    """
    Compute the are enclosed by the maze polygon using shoelace formula:
    https://en.wikipedia.org/wiki/Shoelace_formula
    """
    area = 0
    for idx, n1 in enumerate(nodes):
        n2 = nodes[(idx + 1) % len(nodes)]
        area += (n1.row + n2.row) * (n1.col - n2.col)

    return area // 2


def get_path(steps: list[Step]) -> tuple[list[Node], Grid, int]:
    """
    Construct the vertices from the list of Steps needed to take
    """
    prev_node = Node(0, 0)
    nodes = [prev_node]
    total_length_path = 0
    min_row = 0
    max_row = 0
    min_col = 0
    max_col = 0

    for offset, nsteps in steps:
        total_length_path += nsteps
        new_node = compute_end_vertex(nodes[-1], offset, nsteps)
        nodes.append(new_node)

        # Check for grid edges
        if new_node.row < min_row:
            min_row = new_node.row

        if new_node.row > max_row:
            max_row = new_node.row

        if new_node.col < min_col:
            min_col = new_node.col

        if new_node.col > max_col:
            max_col = new_node.col
        prev_node = new_node

    nodes = nodes[1:]
    return nodes, Grid(min_row, max_row, min_col, max_col), total_length_path


def pick_theorem(path_length: int, area: int) -> int:
    """
    Using the pick theorem too calculate how many nodes are included inside the
    maze polygon:
    https://en.wikipedia.org/wiki/Pick%27s_theorem
    """
    return area + 1 - path_length // 2


def compute(data: str) -> int:
    """Compute the result for the puzzle input"""
    steps = [parse_line(line) for line in data.splitlines()]
    vertices, grid, path_length = get_path(steps)
    # grid.print_path(vertices)
    area = compute_area(vertices)
    nodes_inside = pick_theorem(path_length, area)
    return path_length + nodes_inside


def compute2(data: str) -> int:
    """Compute the result for the puzzle input part 2"""
    steps = [parse_line_color(line) for line in data.splitlines()]
    vertices, grid, path_length = get_path(steps)
    # grid.print_path(vertices)
    area = compute_area(vertices)
    nodes_inside = pick_theorem(path_length, area)
    return path_length + nodes_inside


def main():
    """Run puzzle input"""
    with open("day18_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    result2 = compute2(data)

    print(f"{result=}")
    print(f"{result2=}")


if __name__ == "__main__":
    main()

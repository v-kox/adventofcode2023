""" day 16 helper classes """
from __future__ import annotations

from abc import ABC, abstractmethod
from utils import Offsets


class Lightbeam:
    """Representation of a lightbeam in cell"""

    def __init__(self, row: int, col: int, direction: Offsets):
        self.row = row
        self.col = col
        self.direction = direction

    def move(self, new_direction: Offsets | None = None) -> Lightbeam:
        """
        Move the lightbeam in the provided direction.
        If no direction provided, lightbeam moves in it's current direction
        """
        if new_direction is None:
            new_direction = self.direction

        new_row = self.row + new_direction.value[0]
        new_col = self.col + new_direction.value[1]

        return Lightbeam(new_row, new_col, new_direction)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Lightbeam):
            return (
                self.row == __value.row
                and self.col == __value.col
                and self.direction == __value.direction
            )
        else:
            return False

    def __hash__(self) -> int:
        """ Make it hashable for the seen cache of the grid"""
        return hash((self.row, self.col, self.direction))


class Node(ABC):
    """Generic base class for a Node on the grid"""

    def __init__(self, symbol) -> None:
        self.symbol = symbol
        self.energized = False

    @abstractmethod
    def move_lightbeam(self, lb: Lightbeam) -> list[Lightbeam]:
        """Move the lightbeam based on the properties if the Node"""
        pass

    def set_energized(self) -> None:
        # Energize the Node
        self.energized = True


class EmptyNode(Node):
    """Represents the empty Node, light just passes through"""

    def __init__(self) -> None:
        super().__init__(".")

    def move_lightbeam(self, lb: Lightbeam) -> list[Lightbeam]:
        self.set_energized()
        return [lb.move()]


class HorizontalSplitter(Node):
    """
    Represents the horizontal splitter node.
    If light enters from the north/south it is split into east and west beams.
    If light already from east/west, behaves like en EmptyNode
    """

    def __init__(self) -> None:
        super().__init__("-")

    def move_lightbeam(self, lb: Lightbeam) -> list[Lightbeam]:
        self.set_energized()
        if lb.direction in (Offsets.NORTH, Offsets.SOUTH):
            return [lb.move(Offsets.EAST), lb.move(Offsets.WEST)]
        else:
            return [lb.move()]


class VerticalSplitter(Node):
    """
    Represents the vertical splitter node.
    If light enters from the east/west it is split into north and south beams.
    If light already from north/south, behaves like en EmptyNode
    """

    def __init__(self) -> None:
        super().__init__("|")

    def move_lightbeam(self, lb: Lightbeam) -> list[Lightbeam]:
        self.set_energized()
        if lb.direction in (Offsets.EAST, Offsets.WEST):
            return [lb.move(Offsets.NORTH), lb.move(Offsets.SOUTH)]
        else:
            return [lb.move()]


class MirrorRight(Node):
    """
    Represents the a / mirror node.
    Light takes 90 degree clockwise turn
    """

    def __init__(self) -> None:
        super().__init__("/")

    def move_lightbeam(self, lb: Lightbeam) -> list[Lightbeam]:
        self.set_energized()
        match lb.direction:
            case Offsets.NORTH:
                return [lb.move(Offsets.EAST)]
            case Offsets.EAST:
                return [lb.move(Offsets.NORTH)]
            case Offsets.SOUTH:
                return [lb.move(Offsets.WEST)]
            case Offsets.WEST:
                return [lb.move(Offsets.SOUTH)]

        raise AssertionError(f"Code shoulf be unreachable: {lb}")


class MirrorLeft(Node):
    """
    Represents the a \\ mirror node.
    Light takes 90 degree counter clockwise turn
    """

    def __init__(self) -> None:
        super().__init__("\\")

    def move_lightbeam(self, lb: Lightbeam) -> list[Lightbeam]:
        self.set_energized()
        match lb.direction:
            case Offsets.NORTH:
                return [lb.move(Offsets.WEST)]
            case Offsets.EAST:
                return [lb.move(Offsets.SOUTH)]
            case Offsets.SOUTH:
                return [lb.move(Offsets.EAST)]
            case Offsets.WEST:
                return [lb.move(Offsets.NORTH)]

        raise AssertionError(f"Code should be unreachable: {lb}")


def parse_node(raw_node: str) -> Node:
    """return the correct node type for the given raw node"""
    match raw_node:
        case ".":
            return EmptyNode()
        case "-":
            return HorizontalSplitter()
        case "|":
            return VerticalSplitter()
        case "\\":
            return MirrorLeft()
        case "/":
            return MirrorRight()

    raise AssertionError(f"Code should be unreachable: {raw_node}")


class Grid:
    """representation of the entire grid"""

    def __init__(self, raw_grid: str):
        self.grid = self._parse_grid(raw_grid)

        self.nrows = len(self.grid)
        self.ncols = len(self.grid[0])

        self.energized = [[False] * self.ncols for _ in range(self.nrows)]

        self.lightbeams: list[Lightbeam] = []
        self.seen: set[Lightbeam] = set()

    def _parse_grid(self, raw_grid: str) -> list[list[Node]]:
        """parse raw string grid into grid of nodes"""
        return [[parse_node(c) for c in line] for line in raw_grid.strip().splitlines()]

    def add_lightbeam(self, lb: Lightbeam) -> None:
        """Add a lightbeam to the grid"""
        self.lightbeams.append(lb)

    def remove_lightbeam(self, lb: Lightbeam) -> None:
        """Remove a lightbeam to the grid"""
        self.lightbeams.remove(lb)

    def is_lightbeam_inside_grid(self, lb: Lightbeam) -> bool:
        """Check if a lightbeam is inside the grid"""
        return 0 <= lb.row < self.nrows and 0 <= lb.col < self.ncols

    def get_lightbeam(self) -> Lightbeam:
        return self.lightbeams.pop()

    @property
    def n_energized(self):
        """Return the number of energized nodes"""
        return sum([node.energized for node in line].count(True) for line in self.grid)

    @property
    def raw_grid_energized(self) -> str:
        """
        return a raw string representation of the current situation of energized nodes.
        The current head of the lightbeams are represented with `O`'s
        """
        raw_energized = [
            ["#" if node.energized else "." for node in line] for line in self.grid
        ]

        for lb in self.lightbeams:
            raw_energized[lb.row][lb.col] = "O"

        return "\n".join("".join(line) for line in raw_energized)

    @property
    def raw_grid_symbols(self) -> str:
        """
        return a raw string representation of the grid.
        """
        return "\n".join(
            ["".join([node.symbol for node in line]) for line in self.grid]
        )

    @property
    def has_lightbeams(self) -> bool:
        """check if the grid has lightbeams"""
        return len(self.lightbeams) > 0

    def step(self, lb: Lightbeam) -> list[Lightbeam]:
        """move all lightbeams to their next location"""
        return self.grid[lb.row][lb.col].move_lightbeam(lb)

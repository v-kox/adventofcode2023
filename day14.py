from __future__ import annotations
from utils import Offsets
import pytest

INPUT0 = """\
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
"""

INPUT1 = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

EXPECTED1 = 136
EXPECTED2 = 64

EXPECTED31 = """\
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
"""
EXPECTED32 = """\
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O
"""
EXPECTED33 = """\
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
"""


def test_case0():
    """Test case to calculate scoring"""
    assert compute(INPUT0) == EXPECTED1


def test_case1():
    """Test case example part 1"""
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    assert compute2(INPUT1) == EXPECTED2


@pytest.mark.parametrize(
    "n_cycles, output",
    [
        (0, INPUT1),
        (1, EXPECTED31),
        (2, EXPECTED32),
        (3, EXPECTED33),
    ],
)
def test_case_cycle(n_cycles, output):
    """Test case that cycling platform runs correctly"""
    platform = Platform(INPUT1.strip())

    for _ in range(n_cycles):
        platform = platform.cycle()

    assert platform.raw == output.strip()


class Platform:
    """wrapper class around platform"""

    def __init__(self, raw: str) -> None:
        self.raw = raw

        # construct a grid and get some info about the grid
        self.grid = [[c for c in line] for line in raw.splitlines()]
        self.nrows = len(self.grid)
        self.ncols = len(self.grid[0])

        # element in grid that can move
        self.boulder = "O"
        self.free = "."

    def get_load(self) -> int:
        """Calculate the load for the current grid"""
        return sum(
            (self.nrows - idx) * line.count(self.boulder)
            for idx, line in enumerate(self.grid)
        )

    def tilt(self, offset: Offsets = Offsets.NORTH) -> Platform:
        """Tilt the grid North. Every boulder moves up 1 row if that row is free."""
        new_grid = self.grid.copy()
        for col in range(self.ncols):
            for row in range(self.nrows):
                offset_row = row + offset.value[0]
                offset_col = col + offset.value[1]

                # If offset value outside of grid. Continue
                if (
                    offset_col < 0
                    or offset_col >= self.ncols
                    or offset_row < 0
                    or offset_row >= self.nrows
                ):
                    continue

                if (
                    self.grid[row][col] == self.boulder
                    and self.grid[offset_row][offset_col] == self.free
                ):
                    new_grid[offset_row][offset_col] = self.boulder
                    new_grid[row][col] = self.free

        # Return new tilted platform
        return self._get_platform_from_grid(new_grid)

    def cycle(self) -> Platform:
        """Cycle the platform by tilting it NORTH, WEST, SOUTH and EAST in order."""
        offsets = [Offsets.NORTH, Offsets.WEST, Offsets.SOUTH, Offsets.EAST]
        prev_platform = self._get_platform_from_grid(self.grid)
        for offset in offsets:
            while True:
                new_platform = prev_platform.tilt(offset)
                if new_platform == prev_platform:
                    break
                else:
                    prev_platform = new_platform
        return prev_platform

    @staticmethod
    def _get_platform_from_grid(grid: list[list[str]]) -> Platform:
        """helper method to create new Platform from grid variable"""
        raw = "\n".join(["".join(line) for line in grid])
        return Platform(raw)

    def __eq__(self, that: object) -> bool:
        """Basic equality. If raw platform representation is equal, True"""
        if not isinstance(that, Platform):
            return False
        else:
            return self.raw == that.raw


cache: dict[str, Platform] = {}
cache2: dict[str, int] = {}


def compute(data: str) -> int:
    """Compute puzzle result"""
    platform = Platform(data)
    prev_platform = platform

    # Tilt the platform until no more changes are observed
    while True:
        new_platform = prev_platform.tilt()

        if new_platform == prev_platform:
            break
        else:
            prev_platform = new_platform

    return new_platform.get_load()


def compute2(data: str, n_cycles: int = 1000000000) -> int:
    platform = Platform(data)

    for idx in range(n_cycles):
        if platform.raw in cache:
            # if we find a value we already encountered, get some info on the loop
            # size and break the for loop
            loop_start = cache2[platform.raw]
            loop_length = idx - loop_start
            break

        # If platform not yet in cache , compute cycle and add to cache
        new_platform = platform.cycle()

        cache[platform.raw] = new_platform
        cache2[platform.raw] = idx

        platform = new_platform

    # determine the amount of cycles we still need to do at the end of the n_cycles
    # loop. Assuming we start at the start of the known loop
    rem_cycles = (n_cycles - loop_start) % loop_length
    for _ in range(rem_cycles):
        platform = cache[platform.raw]

    print(f"{loop_start=}, {loop_length}, {rem_cycles}")
    return platform.get_load()


def main():
    """Run puzzle input"""
    with open("day14_input.txt", "r") as f:
        data = f.read()

    import time

    a = time.perf_counter()
    result = compute(data)
    b = time.perf_counter()
    result2 = compute2(data)
    c = time.perf_counter()

    print(f"Time result 1 = {b-a}")
    print(f"Time result 2 = {c-b}")

    print(f"{result=}")
    print(f"{result2=}")


if __name__ == "__main__":
    main()

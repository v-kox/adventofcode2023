from __future__ import annotations

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


def test_case0():
    """Test case to calculate scoring"""
    assert compute(INPUT0) == EXPECTED1


def test_case1():
    """Test case example part 1"""
    assert compute(INPUT1) == EXPECTED1


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

    def tilt(self) -> Platform:
        """Tilt the grid North. Every boulder moves up 1 row if that row is free."""
        new_grid = self.grid.copy()
        for col in range(self.ncols):
            for row in range(1, self.nrows):
                if (
                    self.grid[row][col] == self.boulder
                    and self.grid[row - 1][col] == self.free
                ):
                    new_grid[row - 1][col] = self.boulder
                    new_grid[row][col] = self.free

        # Return new tilted platform
        return self._get_platform_from_grid(new_grid)

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


def main():
    """Run puzzle input"""
    with open("day14_input.txt", "r") as f:
        data = f.read()

    result = compute(data)

    print(f"{result=}")


if __name__ == "__main__":
    main()

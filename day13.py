from __future__ import annotations

INPUT1 = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
"""
EXPECTED1 = 5
EXPECTED5 = 300

INPUT2 = """\
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
EXPECTED2 = 400
EXPECTED6 = 100

INPUT3 = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
EXPECTED3 = 405
EXPECTED7 = 400

INPUT4 = """\
...###.#.....##..
#.######.#.......
#.##.###.#.......
...###.#.....##..
.#..##..#.###..##
#..###.####...###
#####.#...#.##...
#####.#..###.####
#########.#.#####
.#####....##..###
##.#..#..####..##
"""
EXPECTED4 = 16


def test_case1():
    """Test case vertical mirror line"""
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """Test case horizontal mirror line"""
    assert compute(INPUT2) == EXPECTED2


def test_case3():
    """Test case provided example part 1"""
    assert compute(INPUT3) == EXPECTED3


def test_case4():
    """Test case reflect line at the end of the field"""
    assert compute(INPUT4) == EXPECTED4


def test_case5():
    """Test case reflect line at the end of the field"""
    assert compute2(INPUT1) == EXPECTED5


def test_case6():
    """Test case reflect line at the end of the field"""
    assert compute2(INPUT2) == EXPECTED6


def test_case7():
    """Test case reflect line at the end of the field"""
    assert compute2(INPUT3) == EXPECTED7


class Field:
    """wrapper class around lava fields"""

    def __init__(self, grid: list[str]):
        self.grid = grid
        self.ncols = len(grid[0])
        self.nrows = len(grid)

    def _is_reflect(self, idx, max_delta: int = 0) -> bool:
        """
        Return True if the index is a vertical reflect line where the number
        of differences in the reflection is exactly equal to the max_delta
        value provided (default: 0)
        """

        # Compute ranges to check reflection
        r1 = range(idx - 1, max(0, 2 * idx - self.ncols) - 1, -1)
        r2 = range(idx, min(self.ncols, 2 * idx))

        # Count the number of differences in the reflection at the current idx
        delta = 0
        for x, y in zip(r1, r2):
            delta += [s[x] != s[y] for s in self.grid].count(True)

        return delta == max_delta

    def find_reflection(self, max_delta: int = 0) -> int:
        """
        Loop over all columns and return the index of the reflect line.
        i.e. if function returns 5, reflect between 4th and 5th element of field.
        If no reflection found, return 0
        """
        for idx in range(1, self.ncols):
            if self._is_reflect(idx, max_delta):
                return idx

        return 0

    def flip_field(self) -> Field:
        """
        Flip a field 90 degrees, rows becaome columns and vice versa.
        returns a new (flipped) Field
        """
        flipped = [
            "".join([self.grid[row][col] for row in range(self.nrows)])
            for col in range(self.ncols)
        ]

        return Field(flipped)


def read_fields_from_input(data: str) -> list[Field]:
    """Create a list of fields from the input"""
    raw_fields: list[list[str]] = [[]]
    field_idx = 0
    for line in data.splitlines():
        if not line:
            field_idx += 1
            raw_fields.append([])
        else:
            raw_fields[field_idx].append(line)
    return [Field(r) for r in raw_fields]


def compute(data: str) -> int:
    """Compute result part 1"""
    fields = read_fields_from_input(data)

    total = 0

    # Compute reflect for all fields
    for field in fields:
        # Check for a vertical reflect line
        r = field.find_reflection()
        if not r:
            # If no reflect found,
            # Flip field and look for horizontal reflect line
            flipped = field.flip_field()
            r = 100 * flipped.find_reflection()
        total += r
    return total


def compute2(data: str) -> int:
    """Compute result part 1"""
    fields = read_fields_from_input(data)

    total = 0

    # Compute reflect for all fields
    for field in fields:
        # Check for a vertical reflect line
        r = field.find_reflection(max_delta=1)
        if not r:
            # If no reflect found,
            # Flip field and look for horizontal reflect line
            flipped = field.flip_field()
            r = 100 * flipped.find_reflection(max_delta=1)
        total += r
    return total


def main():
    """Run puzzle input"""
    with open("day13_input.txt", "r") as f:
        data = f.read()
    result = compute(data)
    result2 = compute2(data)

    print(f"{result=}")
    print(f"{result2=}")


if __name__ == "__main__":
    main()

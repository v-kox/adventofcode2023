from utils import get_integers_from_line

INPUT1 = """\
0 3 6 9 12 15
"""
EXPECTED1 = 18

INPUT2 = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
EXPECTED2 = 114

INPUT3 = """\
10  13  16  21  30  45
"""
EXPECTED3 = 5

EXPECTED4 = 2


def test_case1():
    """ Test case for 1 row of data """
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """ Test case example part 1 """
    assert compute(INPUT2) == EXPECTED2


def test_case3():
    """ Test case for 1 row of data part 2 """
    assert compute2(INPUT3) == EXPECTED3


def test_case4():
    """ Test case example part 4 """
    assert compute2(INPUT2) == EXPECTED4


def extrapolate(meas: list[int]) -> int:
    """
    Extrapolate the list of measurements

    This is a version of Pascal's Triangle.
    i.s.o. sum, next row is difference between the numbers.

    So the extrapolated value is the last number of each of the previous
    rows. e.g.:
    0   2   4   X
      2   2
        0

    In this case X = 0 + 2 + 4 = 6
    """

    # If all elements are 0, return 0
    if all(x == 0 for x in meas):
        return 0

    # Calculate next row of triangle, by getting the difference between values
    new_vals = [meas[x+1] - meas[x] for x in range(len(meas) - 1)]

    # take the last element of the list and recursively call function
    # with next row of values
    return meas[-1] + extrapolate(new_vals)


def backfill(meas: list[int]) -> int:
    """
    Backfill the list of measurements

    This is a version of Pascal's Triangle.
    i.s.o. sum, next row is difference between the numbers.

    So the backfilled value is the difference between the previous
    filled value and the first element in the row. e.g.:
    A   B
      C
    In this case A = B - C
    """
    # If all elements are 0, return 0
    if all(x == 0 for x in meas):
        return 0

    # Calculate next row of triangle, by getting the difference between values
    new_vals = [meas[x+1] - meas[x] for x in range(len(meas) - 1)]

    # take the last element of the list and recursively call function
    # with next row of values
    return meas[0] - backfill(new_vals)


def compute(data: str) -> int:
    """ Compute the result for part 1 """
    meas = [get_integers_from_line(line) for line in data.splitlines()]

    extrap = [extrapolate(m) for m in meas]
    return sum(extrap)


def compute2(data: str) -> int:
    """ Compute the result for part 2 """
    meas = [get_integers_from_line(line) for line in data.splitlines()]

    backf = [backfill(m) for m in meas]

    return sum(backf)


def main() -> None:
    """ Runnning puzzle input """
    with open("day9_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    result2 = compute2(data)

    print(f"{result=}")
    print(f"{result2=}")


if __name__ == "__main__":
    main()

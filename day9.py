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


def test_case1():
    """ Test case for 1 row of data """
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """ Test case example part 1 """
    assert compute(INPUT2) == EXPECTED2


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


def compute(data: str) -> int:
    """ Compute the result for part 1 """
    meas = [get_integers_from_line(line) for line in data.splitlines()]

    extrap = [extrapolate(m) for m in meas]
    return sum(extrap)


def main() -> None:
    """ Runnning puzzle input """
    with open("day9_input.txt", "r") as f:
        data = f.read()

    result = compute(data)

    print(f"{result=}")


if __name__ == "__main__":
    main()

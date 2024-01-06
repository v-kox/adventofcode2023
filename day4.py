""" Advent of Code 2023 day 4"""
import re

from utils import get_integers_from_line

INPUT1 = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
"""
EXPECTED1 = 8

INPUT2 = """\
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
"""
EXPECTED2 = 1

INPUT3 = """\
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
EXPECTED3 = 0

INPUT4 = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
EXPECTED4 = 13

INPUT5 = """\
Card 1: 9 | 1
"""
EXPECTED5 = 0


def test_case1():
    """ Test case multiple winning numbers """
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """ Test case 1 winning number """
    assert compute(INPUT2) == EXPECTED2


def test_case3():
    """ Test case 0 winning numbers """
    assert compute(INPUT3) == EXPECTED3


def test_case4():
    """ Test case provided test input """
    assert compute(INPUT4) == EXPECTED4


def test_case5():
    """ Test case that card number is not used as winning number """
    assert compute(INPUT5) == EXPECTED5


def calculate_points(win_num: list[int], sel_num: list[int]) -> int:
    """
    Calculate the score based on how many of the
    selected numbers are winning numbers
    """
    scoring_nums = [x for x in sel_num if x in win_num]

    if scoring_nums:
        score = 2**(len(scoring_nums) - 1)
    else:
        score = 0

    return score


def compute(data: str) -> int:
    """ Compute the result of the puzzle """
    total_score = 0
    for line in data.splitlines():
        # Split line on pipe and identify winning and selected numbers
        split_re = r"[|:]"
        split_line = re.split(split_re, line)
        win_num = get_integers_from_line(split_line[1])
        sel_num = get_integers_from_line(split_line[2])

        total_score += calculate_points(win_num, sel_num)

    return total_score


def main() -> None:
    with open("day4_input.txt", "r") as f:
        data = f.read()

    total_score = compute(data)
    print(f"{total_score=}")


if __name__ == '__main__':
    main()

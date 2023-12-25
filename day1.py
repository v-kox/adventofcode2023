import pytest

import re

INPUT = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

EXPECTED = 142

DEBUG = True

def compute(input_str: str) -> int:
    number_regex = r"\d"
    total = 0
    for line in input_str.splitlines():
        numbers = re.findall(number_regex, line)

        # take first and last number
        coord = int(numbers[0] + numbers[-1])

        total += coord

        if DEBUG:
            print(f"{line=}")
            print(f"{numbers=}")
            print(f"{coord=}")
            print(f"{total=}")

    return total

def test_case():
    assert compute(INPUT) == EXPECTED


def main():
    with open("day1_1_input.txt", "r") as f:
        data = f.read()

    total = compute(data)
    print(total)

if __name__ == "__main__":
    main()

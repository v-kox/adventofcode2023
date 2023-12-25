import re

INPUT1 = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

EXPECTED1 = 142

INPUT2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

EXPECTED2 = 281

INPUT3 = """\
sevenine
"""

EXPECTED3 = 79

DEBUG = True


def _find_minmax_index_of_all_matches(line: str, pattern: str) -> list[int]:
    indexes = []

    for m in re.finditer(pattern, line):
        indexes.append(m.start())

    if indexes:
        return (min(indexes), max(indexes))
    else:
        return (len(line)+1, -1)

def get_coordinates_from_line(line: str):
    first_match = len(line) + 1
    last_match = -1

    patterns = {
        "1": r"1|one",
        "2": r"2|two",
        "3": r"3|three",
        "4": r"4|four",
        "5": r"5|five",
        "6": r"6|six",
        "7": r"7|seven",
        "8": r"8|eight",
        "9": r"9|nine",
    }

    for key, pattern in patterns.items():
        min_idx, max_idx = _find_minmax_index_of_all_matches(line, pattern)

        if min_idx < first_match:
            first_match = min_idx
            first_num = key

        if max_idx > last_match:
            last_match = max_idx
            last_num = key

    return int(first_num + last_num)


def compute(input_str: str) -> int:
    total = 0
    for line in input_str.splitlines():
        if DEBUG:
            print(f"{line=}")
        coord = get_coordinates_from_line(line)
        total += coord

        if DEBUG:
            print(f"{coord=}")
            print(f"{total=}")

    return total


def test_case1():
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    assert compute(INPUT2) == EXPECTED2


def test_case3():
    assert compute(INPUT3) == EXPECTED3


def main():
    with open("day1_1_input.txt", "r") as f:
        data = f.read()

    total = compute(data)
    print(total)


if __name__ == "__main__":
    main()

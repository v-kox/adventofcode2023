import re
from typing import Optional

import pytest

INPUT1 = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
EXPECTED1 = 1320
EXPECTED2 = 145

# Regex to get info from raw step string
RE_STEP = re.compile(r"([a-zA-Z]+)([=-])(\d*)")


@pytest.mark.parametrize(
    "char, result",
    [
        ("H", 200),
    ],
)
def test_hash_char(char, result):
    """Test hashing of 1 characted"""
    assert hash_char(char) == result


def test_HASH():
    """test HASH implementation"""
    assert HASH("HASH") == 52


def test_case1():
    """test case example part 1"""
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """test case example part 2"""
    assert compute2(INPUT1) == EXPECTED2


class Step:
    """wrapper class for steps"""

    def __init__(self, symbol: str, operator: str, focal_length: Optional[int] = None):
        self.symbol = symbol
        self.operator = operator
        self.focal_length = focal_length

        # box id is the hash value of the lens symbol
        self.box_idx = HASH(self.symbol)

    def is_insert(self) -> bool:
        return self.operator == "="

    def is_remove(self) -> bool:
        return self.operator == "-"

    def get_step_lens(self) -> tuple[str, int]:
        """
        Get the box representation of the current step.
        If this is an insert step, repr = (symbol, focal_length)
        for a remove step, this function should not be used
        """
        if self.focal_length is None:
            raise AssertionError("Cannot use lens without focal length.")
        return (self.symbol, self.focal_length)


def HASH(data: str):
    """HASH alghoritm of input steps"""
    value = 0

    for c in data:
        value = hash_char(c, value)

    return value


def hash_char(char: str, start_val=0) -> int:
    """Hashing of a single character witha  given start value"""
    hash_val = (17 * (ord(char) + start_val)) % 256

    return hash_val


def parse_step_str(step: str) -> Step:
    """
    Get a Step instance from a raw step string.
    """
    step_data = RE_STEP.match(step)

    if step_data is None:
        raise AssertionError(f"Cannot parse step data from string: {step}")

    symbol = step_data.group(1)
    operator = step_data.group(2)
    focal_length = int(step_data.group(3)) if step_data.group(3) else None

    return Step(symbol, operator, focal_length)


def find_symbol_in_box(symbol: str, box: list[tuple[str, int]]) -> int | None:
    """
    Check if an entry of a lens with symbol already exists in the selected box.
    If so, return the index of the element, otherwise return None
    """
    try:
        return [s == symbol for s, _ in box].index(True)
    except ValueError:
        return None


def HASHMAP(steps: list[str]) -> list[list[tuple[str, int]]]:
    """Implementation HASHMAP alghoritm described in puzzle"""
    # Initilize boxes
    hashmap: list[list[tuple[str, int]]] = [[] for _ in range(256)]

    for raw_step in steps:
        step = parse_step_str(raw_step)
        idx = find_symbol_in_box(step.symbol, hashmap[step.box_idx])

        # If the step is a remove step, attempt to remove from box
        if step.is_remove():
            if idx is not None:
                hashmap[step.box_idx].pop(idx)
            continue
        else:
            # If element doesnt already exist in box, append to box
            # else replace existing lens with one from this step
            if idx is None:
                hashmap[step.box_idx].append(step.get_step_lens())
            else:
                hashmap[step.box_idx][idx] = step.get_step_lens()

    return hashmap


def calc_focus_power(boxes: list[list[tuple[str, int]]]) -> list[int]:
    """Calculate the focus power of all lenses"""
    focus_power: list[int] = []

    for box_idx, box in enumerate(boxes):
        focus_power.append(
            sum(
                (1 + box_idx) * (1 + lens_idx) * lens[1]
                for lens_idx, lens in enumerate(box)
            )
        )

    return focus_power


def compute(data: str) -> int:
    """Compute puzzle output"""
    steps = data.strip().split(",")

    return sum(HASH(step) for step in steps)


def compute2(data: str) -> int:
    """compute puzzle output part 2"""
    steps = data.strip().split(",")

    hashmap = HASHMAP(steps)
    focus_power = calc_focus_power(hashmap)
    return sum(focus_power)


def main():
    """Run puzzle input"""
    with open("day15_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    result2 = compute2(data)

    print(f"{result=}")
    print(f"{result2=}")


if __name__ == "__main__":
    main()

""" Advent of Code 2023 day3 """
from __future__ import annotations

import re
from dataclasses import dataclass
from dataclasses import field

INPUT1 = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

EXPECTED1 = 4361
EXPECTED2 = 467835

def test_case1():
    """ test day3 part 1"""
    assert compute(INPUT1) == EXPECTED1

def test_case2():
    """ test day3 part 2"""
    assert compute2(INPUT1) == EXPECTED2

@dataclass
class Symbol:
    """ Dataclass for symbol in grid """
    value: str
    row: int
    col: int
    mask: list[tuple[int, int]]
    adj_num: list[GridNumber] = field(default_factory=list)

    def is_num_adj(self, num: GridNumber) -> bool:
        """ return True if gridnumber adjacent to this Symbol """
        return any([c in self.mask for c in num.coords])

@dataclass
class GridNumber:
    """ Dataclass for number in grid """
    value: int  # the actual value
    row: int    # row index
    cols: list[int] # all column indexes that contain a number

    @property
    def coords(self) -> list[tuple[int, int]]:
        """ return a list of grid coords of the GridNumber """
        return [(x, self.row) for x in self.cols]

    def is_valid(self, symbols: list[Symbol]) -> bool:
        """ return True if GridNumber adjacent to any of the symbols """
        return any(s.is_num_adj(self) for s in symbols)

def _read_numbers_from_line(line: str, rown: int) -> list[GridNumber]:
    """ Returns the GridNumbers from a line in the grid """
    number_regex = r"\d+"
    return [
        GridNumber(
            value = int(m.group()),
            row = rown,
            cols = list(range(m.span()[0], m.span()[1]))
        )
        for m in re.finditer(number_regex, line)
    ]

def _read_symbols_from_line(line: str, rown: int) -> list[Symbol]:
    """ reads symbols from line in the grid and returns Symbol instances """
    symbol_regex = r"[^\d\.\n]{1}"
    return [
        Symbol(
            value = m.group(),
            row = rown,
            col = m.span()[0],
            mask = _get_mask_around_symbol(rown, m.span()[0]),
        )
        for m in re.finditer(symbol_regex, line)
    ]

def _get_mask_around_symbol(row: int, col: int) -> list[tuple[int, int]]:
    """ helper function to return list of coordinates around a grid point """
    return [
        (x, y)
        for y in range(row-1, row+2)
        for x in range(col-1, col+2)
        ]

def get_numbers_around_symbol(s: Symbol, numbers: list[GridNumber]) -> list[GridNumber]:
    """ Returns a list of GridNumbers which are adjacent to the Symbol. """
    return [n for n in numbers if s.is_num_adj(n)]

def compute(data: str) -> int:
    """ compute function to run day 3 part 1 """
    numbers: list[GridNumber] = []
    symbols: list[Symbol] = []
    for rown, line in enumerate(data.splitlines()):
        numbers += _read_numbers_from_line(line, rown)
        symbols += _read_symbols_from_line(line, rown)

    valid_numbers = [n for n in numbers if n.is_valid(symbols)]

    return sum([x.value for x in valid_numbers])

def compute2(data: str) -> int:
    """ compute function to run day 3 part 2 """
    numbers: list[GridNumber] = []
    symbols: list[Symbol] = []
    for rown, line in enumerate(data.splitlines()):
        numbers += _read_numbers_from_line(line, rown)
        symbols += _read_symbols_from_line(line, rown)

    adj = [get_numbers_around_symbol(s, numbers) for s in symbols]

    return sum([a[0].value * a[1].value for a in adj if len(a) == 2])

def main() -> None:
    with open("day3_input.txt", "r") as f:
        data = f.read()

    total = compute(data)
    print(f"{total=}")

    total2 = compute2(data)
    print(f"{total2=}")

if __name__ == "__main__":
    main()

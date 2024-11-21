""" Advent of Code 2023 day 4"""
import re
from dataclasses import dataclass

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
EXPECTED6 = 30  # Ouput for part 2

INPUT5 = """\
Card 1: 9 | 1
"""
EXPECTED5 = 0

INPUT7 = """\
Card 1: 1 2 3 | 1 2 3
Card 2: 1 2 3 | 9 8 7
Card 3: 1 2 3 | 9 8 7
Card 4: 1 2 3 | 9 8 7
"""
EXPECTED7 = 7

INPUT8 = """\
Card 1: 1 2 3 | 1 2 3
Card 2: 1 2 3 | 1 2 3
Card 3: 1 2 3 | 1 2 3
Card 4: 1 2 3 | 1 2 3
"""
EXPECTED8 = 15


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


def test_case6():
    """ Test case for test input part 2 """
    assert compute2(INPUT4) == EXPECTED6


def test_case7():
    """ Test case part 2. First card all winners, rest no winners """
    assert compute2(INPUT7) == EXPECTED7


def test_case8():
    """
    Test case part 2. Worst case scenario all winners. (for performance)
    """
    assert compute2(INPUT8) == EXPECTED8


@dataclass
class ScratchCard:
    """ Representation of a ScratchCard """
    id: int
    win_nums: list[int]
    sel_nums: list[int]

    @property
    def scoring_numbers(self) -> list[int]:
        """
        Returns the list of selected numbers that are also
        winning numbers
        """
        return [x for x in self.sel_nums if x in self.win_nums]

    @property
    def score(self) -> int:
        """ Returns the score of the ScratchCard"""
        if not self.scoring_numbers:
            score = 0
        else:
            score = 2 ** (self.n_scoring - 1)
        return score

    @property
    def n_scoring(self) -> int:
        """ returns the number of scoring numbers """
        return len(self.scoring_numbers)


def get_scratch_card_from_line(line: str) -> ScratchCard:
    """ Parse a line of input and return a ScratchCard object """

    # Split line on pipe and identify winning and selected numbers
    split_re = r"[|:]"
    split_line = re.split(split_re, line)

    card_idx = get_integers_from_line(split_line[0])
    win_num = get_integers_from_line(split_line[1])
    sel_num = get_integers_from_line(split_line[2])

    return ScratchCard(card_idx[0], win_num, sel_num)


def compute(data: str) -> int:
    """ Compute the result of the puzzle """
    total_score = 0
    for line in data.splitlines():
        card = get_scratch_card_from_line(line)

        total_score += card.score

    return total_score


def compute2(data: str) -> int:
    """ Compute the result of part 2 """
    cards = [
        get_scratch_card_from_line(line)
        for line in data.splitlines()
        ]

    # initially start with 1 occurence of each card
    n_cards = [1 for _ in range(len(cards))]

    for idx, card in enumerate(cards):
        if card.n_scoring:
            # Get the start and end index of the slice of the n_cards
            # array we need to update
            start_idx = idx + 1
            end_idx = min(idx + card.n_scoring + 1, len(cards))
            for idx2 in range(start_idx, end_idx):
                # Based on the number of occurences of the current card,
                # We can add how many times it will add subsequent cards
                n_cards[idx2] += n_cards[idx]

    # return the sum of occurences of each scratch card
    return sum(n_cards)


def main() -> None:
    with open("day4_input.txt", "r") as f:
        data = f.read()

    total_score = compute(data)
    print(f"{total_score=}")

    n_cards = compute2(data)
    print(f"{n_cards=}")


if __name__ == '__main__':
    main()

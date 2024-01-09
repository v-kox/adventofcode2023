""" Advent of Code 2023 day 7 """

from dataclasses import dataclass
from enum import IntEnum

import pytest

from utils import get_integers_from_line

INPUT1 = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
EXPECTED1 = 6440
EXPECTED2 = 5905

CARD_VALUES = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

CARD_VALUES_WILDCARD = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


class HandStrength(IntEnum):
    """ Enum representing hand strength """
    FIVE = 7
    FOUR = 6
    FULLHOUSE = 5
    THREE = 4
    TWOPAIR = 3
    PAIR = 2
    HIGH = 1


@dataclass
class Hand:
    """ representation of a Camel Cards hand """
    cards: str
    bid: int = 0

    def _strength_from_count(self, card_counts: list[int]) -> HandStrength:
        """
        Return the hand strength based on a list of counts of occurences
        """
        sorted_count = sorted(card_counts, reverse=True)
        match len(sorted_count):
            case 1:
                strength = HandStrength.FIVE
            case 2 if sorted_count[0] == 4:
                strength = HandStrength.FOUR
            case 2:
                strength = HandStrength.FULLHOUSE
            case 3 if sorted_count[0] == 3:
                strength = HandStrength.THREE
            case 3:
                strength = HandStrength.TWOPAIR
            case 4:
                strength = HandStrength.PAIR
            case 5:
                strength = HandStrength.HIGH
            case _:
                raise ValueError(f"Incorrect hand received: {self.cards}")
        return strength

    @property
    def hand_strength(self) -> HandStrength:
        """ Determine the strength of the hand """
        unique_chars = set(self.cards)
        counted_chars = [self.cards.count(c) for c in unique_chars]

        return self._strength_from_count(counted_chars)

    @property
    def card_values(self) -> list[int]:
        """ Returns a list of the values of the cards in the hand. """
        return [CARD_VALUES[x] for x in self.cards]

    def __lt__(self, other) -> bool:
        """ Less Than function for sorting """
        if self.cards == other.cards:
            return False
        elif self.hand_strength == other.hand_strength:
            return self.card_values < other.card_values
        else:
            return self.hand_strength < other.hand_strength

    def __le__(self, other) -> bool:
        """ Less Than or Equal function for sorting """
        return self.cards == other.cards or self < other

    def __gt__(self, other) -> bool:
        """ Greater Than function for sorting """
        return not self <= other

    def __ge__(self, other) -> bool:
        """ Greater Than or Equal function for sorting """
        return not self < other


@dataclass
class HandWildCard(Hand):
    """ Representation of a Camel Cards hand with J as wildcard """

    wildcard: str = "J"

    @property
    def n_wildcards(self) -> int:
        """ Returns the number of wildcards in the hand. """
        return self.cards.count(self.wildcard)

    @property
    def card_values(self) -> list[int]:
        """ Returns a list of the values of the cards in the hand. """
        return [CARD_VALUES_WILDCARD[x] for x in self.cards]

    @property
    def hand_strength(self) -> HandStrength:
        """ Determine the strength of the hand """
        unique_chars = set(self.cards)

        # Count non-wildcard characters
        counted_chars = sorted(
            [
                self.cards.count(c)
                for c in unique_chars
                if c != self.wildcard
            ],
            reverse=True)

        if not counted_chars:
            # If list is empty, all characters all wildcards
            counted_chars.append(self.n_wildcards)
        else:
            # Add the number of wildcards to the other card that has
            # the highest occurence. As this will increase the card
            # strength the most
            counted_chars[0] += self.n_wildcards

        return self._strength_from_count(counted_chars)


def test_case1():
    """ Test case part 1 example """
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """ Test case part 2 example """
    assert compute2(INPUT1) == EXPECTED2


@pytest.mark.parametrize(
        "card, strength",
        [
            (Hand("AAAAA"), HandStrength.FIVE),
            (Hand("AAAAK"), HandStrength.FOUR),
            (Hand("AAAKK"), HandStrength.FULLHOUSE),
            (Hand("AAAKQ"), HandStrength.THREE),
            (Hand("AAKKQ"), HandStrength.TWOPAIR),
            (Hand("AAKQJ"), HandStrength.PAIR),
            (Hand("AKQJT"), HandStrength.HIGH),
        ])
def test_hand_strength(card: Hand, strength: HandStrength):
    """ Test the handstrength calculation """
    assert card.hand_strength == strength


def parse_hand(line: str) -> Hand:
    """ Parse the Hand defined by the line """
    split_line = line.split(" ")
    cards = split_line[0]
    bid = get_integers_from_line(split_line[1])
    return Hand(cards, bid[0])


def parse_wildcard_hand(line: str) -> HandWildCard:
    """ Parse the WildcardHand defined by the line """
    split_line = line.split(" ")
    cards = split_line[0]
    bid = get_integers_from_line(split_line[1])
    return HandWildCard(cards, bid[0])


def compute(data: str) -> int:
    """ Compute the result for part 1 """
    hands = [parse_hand(line) for line in data.splitlines()]
    sorted_hands = sorted(hands)
    total_score = 0
    for rank, hand in enumerate(sorted_hands):
        total_score += (rank + 1) * hand.bid

    return total_score


def compute2(data: str) -> int:
    """ Compute the result for part 2 """
    hands = [parse_wildcard_hand(line) for line in data.splitlines()]
    sorted_hands = sorted(hands)
    # breakpoint()
    total_score = 0
    for rank, hand in enumerate(sorted_hands):
        total_score += (rank + 1) * hand.bid

    return total_score


def main() -> None:
    """ Runnning puzzle input """
    with open("day7_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    result2 = compute2(data)

    print(f"{result=}")
    print(f"{result2=}")


if __name__ == "__main__":
    main()

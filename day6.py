""" Advent of Code 2023 day 6 """

from dataclasses import dataclass

from utils import get_integers_from_line, get_numbers_from_line

INPUT1 = """\
Time:      7  15   30
Distance:  9  40  200
"""

EXPECTED1 = 288
EXPECTED2 = 71503


def test_case1():
    """ Test case for example in part 1 p"""
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """ Test case for example in part 2 """
    assert compute2(INPUT1) == EXPECTED2


@dataclass
class Race:
    """ Representation of a boat race """
    time: int
    record_distance: int

    acceleration: int = 1
    start_speed: int = 0

    def get_distance_all_strategies(self) -> list[int]:
        """
        Return the distance traveled for each strategy
        assuming linear acceleration
        """
        return [
            (self.time - x) * (self.start_speed + x * self.acceleration)
            for x in range(self.time + 1)
            ]

    def get_strategies_beat_record(self) -> list[int]:
        """
        Return distances traveled for each strategy that beats the
        record distance.
        """
        return [
            x
            for x in self.get_distance_all_strategies()
            if x > self.record_distance
            ]


def compute(data: str) -> int:
    """ Compute function for part 1 """
    for line in data.splitlines():
        if line.startswith("Time"):
            times = get_integers_from_line(line)
        elif line.startswith("Distance"):
            distances = get_integers_from_line(line)
        else:
            raise ValueError(f"Don't know how to parse '{line}'")

    races = [Race(time=t, record_distance=r) for t, r in zip(times, distances)]
    winning_races = [r.get_strategies_beat_record() for r in races]

    output = 1
    for win_rac in winning_races:
        output *= len(win_rac)

    return output


def compute2(data: str) -> int:
    """ Compute function for part 1 """
    for line in data.splitlines():
        if line.startswith("Time"):
            times = get_numbers_from_line(line)
            time = int("".join(times))
        elif line.startswith("Distance"):
            distances = get_numbers_from_line(line)
            distance = int("".join(distances))
        else:
            raise ValueError(f"Don't know how to parse '{line}'")

    race = Race(time=time, record_distance=distance)
    winning_races = race.get_strategies_beat_record()

    return len(winning_races)


def main() -> None:
    """ Runnning puzzle input """
    with open("day6_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    result2 = compute2(data)

    print(f"{result=}")
    print(f"{result2=}")


if __name__ == '__main__':
    main()

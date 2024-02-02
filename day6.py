""" Advent of Code 2023 day 6 """

import math
from dataclasses import dataclass

from utils import get_integers_from_line
from utils import get_numbers_from_line

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
    """
    Representation of a boat race

    The distance traveled based on how long you accelerate is a
    quadratic function that can be presented as: -x * (x - t)
    where t is the time in the race.
    """
    time: int
    record_distance: int

    def calculate_distance(self, t: int) -> int:
        """
        Returns the distance traveled for a givent acceleration
        period t
        """
        return -t * (t + self.time)

    def get_range_to_beat_record(self) -> range:
        """
        This function returns the range in which the distance
        traveled in the race beats the record distance.

        Since the distance traveled is a quadratic function, the start and end
        of the range is where that function intersects with the function y = d
        where d is the record distance.

        Intersection points can be calculated using the following formula:

        x = (t ± √(t**2 - 4 * d)) / 2
        """
        t = self.time
        d = self.record_distance + 1
        x_start = math.ceil((t - math.sqrt(t**2 - 4 * d)) / 2)
        x_end = math.floor((t + math.sqrt(t**2 - 4 * d)) / 2)

        return range(x_start, x_end + 1)


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
    winning_races = [r.get_range_to_beat_record() for r in races]

    output = 1
    for win_rac in winning_races:
        output *= (win_rac.stop - win_rac.start)

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

    win_range = race.get_range_to_beat_record()

    return win_range.stop - win_range.start


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

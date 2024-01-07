""" Advent of Code 2023 day 5 """
import re
from dataclasses import dataclass, field
from typing import Optional

from utils import get_integers_from_line

INPUT1 = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
EXPECTED1 = 35


def test_case1():
    """ Test example data given """
    assert compute(INPUT1) == EXPECTED1


@dataclass
class AlmanacMap:
    """ Representation of the farming almanac """
    name: str
    source: list[int] = field(default_factory=list)
    dest: list[int] = field(default_factory=list)
    length: list[int] = field(default_factory=list)

    def _find_idx_in_ranges(self, src: int) -> Optional[int]:
        """
        Checks is any of the give ranges contain the src value.
        This function returns the index of the range defined by
        self.source[idx] and self.length[idx]
        """
        result = None
        for idx, (x, y) in enumerate(zip(self.source, self.length)):
            if x <= src <= x + y - 1:
                result = idx
                break

        return result

    def get_dest(self, src: int) -> int:
        """ Return the destination for a given source value """
        idx = self._find_idx_in_ranges(src)

        # If src not in any range, return the same value
        if not idx:
            return src

        return self.dest[idx] + (src - self.source[idx])


def construct_map(
        dest_start: int,
        source_start: int,
        length: int,
        ) -> dict[int, int]:
    """
    Construct the map segment defined by source and dest start with given
    length
    """
    return {
        (source_start + x): dest_start + x
        for x in range(length)
        }


def find_min_location(
        idxs: list[int],
        maps: dict[str, AlmanacMap],
        map_order: list[str],
        ) -> int:
    """
    Given a list of indexes, maps and a map_order. Returns the minimum value
    of the final map for the input indexes.
    """
    if not map_order:
        return min(idxs)

    # breakpoint()
    this_map = maps[map_order[0]]
    new_idxs = [this_map.get_dest(x) for x in idxs]

    return find_min_location(new_idxs, maps, map_order[1:])


def compute(data: str) -> int:
    """ Compute function for part 1 """
    maps: dict[str, AlmanacMap] = {}

    mapnames = [
        "seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
        "water-to-light", "light-to-temperature", "temperature-to-humidity",
        "humidity-to-location"
    ]

    for line in data.splitlines():
        if not line.strip():
            continue
        elif line.startswith("seeds:"):
            seeds = get_integers_from_line(line)
        elif "map:" in line:
            map_name_re = r"(\S+)"
            match = re.match(map_name_re, line)

            if not match:
                continue
            else:
                map_name = match.group()

            if map_name not in maps:
                maps[map_name] = AlmanacMap(name=map_name)
        else:
            nums = get_integers_from_line(line)
            maps[map_name].dest.append(nums[0])
            maps[map_name].source.append(nums[1])
            maps[map_name].length.append(nums[2])

    res = find_min_location(seeds, maps, mapnames)
    return res


def main() -> None:
    """ Runnning puzzle input """
    with open("day5_input.txt", "r") as f:
        data = f.read()

    result = compute(data)

    print(f"{result=}")


if __name__ == '__main__':
    main()

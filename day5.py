""" Advent of Code 2023 day 5 """
import re
from dataclasses import dataclass
from dataclasses import field
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
EXPECTED2 = 46


def test_case1():
    """ Test example data given """
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """ Test example giver part 2 """
    assert compute2(INPUT1) == EXPECTED2


@dataclass
class AlmanacMap:
    """ Representation of the farming almanac """
    name: str
    _source: list[int] = field(default_factory=list)
    _dest: list[int] = field(default_factory=list)
    _length: list[int] = field(default_factory=list)

    def add(self, source: int, dest: int, length: int) -> None:
        """ Add more map data to the alamanac """
        self._source.append(source)
        self._dest.append(dest)
        self._length.append(length)

    @property
    def source(self) -> list[int]:
        """ Return sorted version of sources """
        return sorted(self._source)

    @property
    def dest(self) -> list[int]:
        """ Return dest sorted by source """
        temp = sorted(zip(self._source, self._dest))
        return [x for _, x in temp]

    @property
    def length(self) -> list[int]:
        """ Return length sorted by source """
        temp = sorted(zip(self._source, self._length))
        return [x for _, x in temp]

    def _find_idx_in_ranges(self, src: int) -> Optional[int]:
        """
        Checks if any of the almanac source ranges contain the src value.
        This function returns the index of the range defined by
        self.source[idx]
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
        if idx is None:
            return src

        return self.dest[idx] + (src - self.source[idx])

    def get_dest_range(self, source_range: range) -> list[range]:
        """
        Given a range of sources, compute the  corresponding output ranges.

        Note that for a given input range the output can be multiple ranges.
        But the total length of the ranges should be the same as the input
        range.
        """
        start = source_range.start
        end = source_range.stop

        # First range boundary is the start value of the input range
        range_boundaries = [start]

        # Loop over all ranges in the almanac to determine boundaries
        for idx, x in enumerate(self.source):
            if x >= end or x + self.length[idx] < start:
                # If a range starts after the input range, or ends
                # before it starts. Skip it.
                continue

            if start < x < end:
                # If start of range in the input range, add it to boundary list
                range_boundaries.append(x)

            if x + self.length[idx] < end:
                # if end of range inside the input range, add it to the list
                range_boundaries.append(x + self.length[idx])

        # Add the end of the input range to the boundary list
        range_boundaries.append(end)

        # Generate the output ranges based on the previously computed
        # range boundaries
        output = []
        for idx in range(0, len(range_boundaries) - 1, 2):
            if range_boundaries[idx] == range_boundaries[idx+1]:
                # This is purely to avoid some small scenarios where
                # we get an empty range. e.g. range(5,5)
                continue

            new_start = self.get_dest(range_boundaries[idx])

            # To get the end value of the range end, we need to calculate the
            # dest value 1 before the boundary (otherwise that value van lie
            # in a diffetent range) and then add 1 again, to keep the correct
            # length of the generator
            new_stop = self.get_dest(range_boundaries[idx+1] - 1) + 1
            output.append(range(new_start, new_stop))

        return output


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

    this_map = maps[map_order[0]]
    new_idxs = [this_map.get_dest(x) for x in idxs]
    return find_min_location(new_idxs, maps, map_order[1:])


def find_min_location_range(
        idx: list[range],
        maps: dict[str, AlmanacMap],
        map_order: list[str],
        ) -> int:
    """
    Given a list of indexes, maps and a map_order. Returns the minimum value
    of the final map for the input indexes.
    """
    if not map_order:
        return min([x.start for x in idx])

    this_map = maps[map_order[0]]

    new_ranges = []
    for r in idx:
        new_ranges += this_map.get_dest_range(r)

    return find_min_location_range(new_ranges, maps, map_order[1:])


def _parse_almanac(data: str) -> tuple[list[int], dict[str, AlmanacMap]]:
    """ helper function that parses the input data """
    maps: dict[str, AlmanacMap] = {}

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

            maps[map_name].add(dest=nums[0], source=nums[1], length=nums[2])

    return seeds, maps


def compute(data: str) -> int:
    """ Compute function for part 1 """
    mapnames = [
        "seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
        "water-to-light", "light-to-temperature", "temperature-to-humidity",
        "humidity-to-location"
    ]

    seeds, maps = _parse_almanac(data)

    res = find_min_location(seeds, maps, mapnames)
    return res


def compute2(data: str):
    """ Compute function for part 2 """
    mapnames = [
        "seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
        "water-to-light", "light-to-temperature", "temperature-to-humidity",
        "humidity-to-location"
    ]

    seeds, maps = _parse_almanac(data)
    seed_ranges = [
        range(seeds[x], seeds[x] + seeds[x+1])
        for x in range(0, len(seeds), 2)
        ]

    res = find_min_location_range(seed_ranges, maps, mapnames)
    return res


def main() -> None:
    """ Runnning puzzle input """
    with open("day5_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    result2 = compute2(data)

    print(f"{result=}")
    print(f"{result2=}")


if __name__ == '__main__':
    main()

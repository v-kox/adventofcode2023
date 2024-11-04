from __future__ import annotations

from dataclasses import dataclass
from typing import Generator
from typing import List
from typing import Set
from typing import Tuple

import pytest

INPUT1 = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""
EXPECTED1 = 5


@pytest.mark.parametrize(
    "x1, x2, y1, y2",
    [
        (1, 1, 2, 2),
        (1, 2, 3, 4),
        (5, 4, 3, 2),
        (999, 888, 777, 555),
    ],
)
def test_brick_not_vertical(x1: int, x2: int, y1: int, y2: int):
    import random

    z = random.randint(0, 10000)
    brick = Brick(x=(x1, x2), y=(y1, y2), z=(z, z))

    assert not brick.is_vertical


@pytest.mark.parametrize(
    "z1, z2",
    [
        (1, 2),
        (3, 4),
        (1, 1000),
    ],
)
def test_brick_vertical(z1: int, z2: int):
    import random

    x = random.randint(1, 100000)
    y = random.randint(1, 100000)
    brick = Brick(x=(x, x), y=(y, y), z=(z1, z2))

    assert brick.is_vertical


def test_graph():
    brick = Brick((1, 2), (2, 2), (2, 2))
    graph = Graph()

    drop_b1 = graph.add_brick(brick)

    supported_by = graph.get_supported_by(drop_b1)
    supports = graph.get_supports(drop_b1)

    assert len(supported_by) == 1
    assert len(supports) == 0
    assert supported_by[0].is_ground


def test_graph_supports():
    brick1 = Brick((1, 2), (2, 2), (2, 2))
    brick2 = Brick((1, 2), (3, 3), (5, 5))
    brick3 = Brick((1, 1), (2, 3), (7, 7))
    graph = Graph()
    drop_b1 = graph.add_brick(brick1)
    drop_b2 = graph.add_brick(brick2)
    drop_b3 = graph.add_brick(brick3)

    supported_by = graph.get_supported_by(drop_b3)

    # Check dropped coordinates
    assert drop_b3.z == (2, 2)
    assert drop_b3.x == brick3.x
    assert drop_b3.y == brick3.y

    # Check that brick 3 is suppored by bricks 1 and 2
    assert len(supported_by) == 2
    assert drop_b1 in supported_by
    assert drop_b2 in supported_by


def test_support_on_vertical_brick():
    brick1 = Brick((1, 1), (1, 1), (5, 10))
    brick2 = Brick((1, 1), (1, 10), (11, 11))

    graph = Graph()

    drop_b1 = graph.add_brick(brick1)
    drop_b2 = graph.add_brick(brick2)

    # Check that b2 is only supported by dropped brick 1
    b2_supported = graph.get_supported_by(drop_b2)
    assert len(b2_supported) == 1
    assert drop_b1 in b2_supported

    # Check that height is set properly
    assert drop_b2.z == (7, 7)


def test_case1():
    """Test case for example part 1"""
    assert compute(INPUT1) == EXPECTED1


@dataclass(frozen=True, eq=True)
class Brick:
    x: Tuple[int, int]
    y: Tuple[int, int]
    z: Tuple[int, int]

    def drop(self, z: int) -> Brick:
        """
        Drop the block to z-coordinate
        """
        old_z = self.z[0]
        new_z = (z, self.z[1] - (old_z - z))

        return Brick(x=self.x, y=self.y, z=new_z)

    @property
    def is_vertical(self) -> bool:
        """
        Check if the current brick is vertical
        """
        return (
            self.x[0] == self.x[1] and self.y[0] == self.y[1] and self.z[0] != self.z[1]
        )

    def get_blocks(self) -> Generator[Tuple[int, int, int], None, None]:
        for x in range(self.x[0], self.x[1] + 1):
            for y in range(self.y[0], self.y[1] + 1):
                for z in range(self.z[0], self.z[1] + 1):
                    yield (x, y, z)

    @property
    def is_ground(self) -> bool:
        return max(self.z) == 0


class Graph:
    def __init__(self) -> None:
        self.bricks: List[Brick] = []
        self._ground = Brick((0, 0), (0, 0), (0, 0))
        self._supported_by: dict[Brick, List[Brick]] = {}
        self._supports: dict[Brick, List[Brick]] = {self._ground: []}
        self._coord_support: dict[Tuple[int, int], Brick] = {}

    def add_brick(self, brick: Brick) -> Brick:
        """
        Drops the brick as low as possible.
        Inserts it into the grapg struct.

        returns the dropped Brick object
        """
        height, supports = self._find_supporting_bricks(brick)

        # brick will drop to z value 1 higher than the support bricks
        new_z = height + 1
        dropped_brick = brick.drop(new_z)

        # update the supported_by dictionary
        self._supported_by[dropped_brick] = list(supports)

        # update the coord_support map
        for x, y, _ in brick.get_blocks():
            self._coord_support[(x, y)] = dropped_brick

        # For each support indicate that it supports current brick
        for support in supports:
            self.get_supports(support).append(dropped_brick)

        # When adding brick, it doesn't support anything yet
        self._supports[dropped_brick] = []
        self.bricks.append(dropped_brick)

        return dropped_brick

    def _find_supporting_bricks(self, brick: Brick) -> Tuple[int, Set[Brick]]:
        """
        Return a set of Bricks that will be supporting the current brick
        """
        if brick.is_vertical:
            result = self._get_support_coord(brick.x[0], brick.y[0])
            return result.z[1], {result}
        else:
            # For all coordinates of the brick find the current brick that is supporting
            # that coordinate
            z = [self._get_support_coord(x, y) for x, y, _ in brick.get_blocks()]

            # check the max z value and return set of items where z-value == max_z
            max_z = max(b.z[1] for b in z)

            return max_z, set([b for b in z if b.z[1] == max_z])

    def _get_support_coord(self, x: int, y: int) -> Brick:
        """
        Return the brick that is currently supporting on coordinate (x, y)
        """
        if (x, y) not in self._coord_support:
            self._coord_support[(x, y)] = self._ground

        return self._coord_support[(x, y)]

    def get_supported_by(self, brick: Brick) -> List[Brick]:
        """
        Return a list of Bricks that are supporting the current brick
        """
        return self._supported_by.get(brick, [])

    def get_supports(self, brick: Brick) -> List[Brick]:
        """
        Return a list of bricks that are supported by this Brick.
        """
        return self._supports.get(brick, [])

    def get_bricks_safe_to_disintegrate(self) -> Set[Brick]:
        """
        Returns a set of bricks that are safe to disintegrate.

        A brick is safe to disintegrate if deleting it doesn't move any other bricks.
        e.g. it doesn't support any other brick, or all bricks that it supports have at least
        1 more support
        """
        safe_bricks = []

        for brick in self.bricks:
            supports = self.get_supports(brick)

            # This brick doesn't support anything. So can be disintegrated
            if len(supports) == 0:
                safe_bricks.append(brick)
                continue

            # If all bricks that are supported by the current brick,
            # are supported by at least one other brick.
            # This brick can be disintegrated
            n_supported_by = [len(self.get_supported_by(x)) for x in supports]

            if all(x > 1 for x in n_supported_by):
                safe_bricks.append(brick)

        return set(safe_bricks)


def parse_line(line: str) -> Brick:
    start, stop = line.split("~", maxsplit=1)
    start_coord = [int(x) for x in start.split(",", maxsplit=2)]
    stop_coord = [int(x) for x in stop.split(",", maxsplit=2)]

    return Brick(
        x=(start_coord[0], stop_coord[0]),
        y=(start_coord[1], stop_coord[1]),
        z=(start_coord[2], stop_coord[2]),
    )


def parse_graph(data: str) -> Graph:
    """
    Parse each line into a brick, and construct the graph
    """
    graph = Graph()
    bricks = [parse_line(line) for line in data.splitlines()]
    # Need to sort by z coordinate so that lowest ones are dropped first
    bricks.sort(key=lambda x: x.z)
    [graph.add_brick(brick) for brick in bricks]

    return graph


def compute(data: str) -> int:
    graph = parse_graph(data)

    safe_bricks = graph.get_bricks_safe_to_disintegrate()
    return len(safe_bricks)


def main() -> None:
    """Runnning puzzle input"""
    with open("day22_input.txt", "r") as f:
        data = f.read()

    result = compute(data)

    print(f"{result=}")


if __name__ == "__main__":
    main()

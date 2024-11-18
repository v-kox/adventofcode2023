from __future__ import annotations

from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Tuple

INPUT1 = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""
LIMIT1 = (7, 27)
EXPECTED1 = 2


def test_case1():
    assert compute(INPUT1, LIMIT1) == EXPECTED1


@dataclass
class Line:
    point: Tuple[int, int, int]
    direction: Tuple[int, int, int]

    def get_point_at_lambda(self, lamda: float) -> Tuple[float, float, float]:
        """
        Returns the coordinates of the function for a given lambda value, where lambda
        is used to parameterize the line in #d space:
        lambda = (x - x1) / alpha = (y - y1) / beta = (z - z1) / gamma
        """
        x = self.direction[0] * lamda + self.point[0]
        y = self.direction[1] * lamda + self.point[1]
        z = self.direction[2] * lamda + self.point[2]

        return (x, y, z)

    def intersects(self, other: Line) -> Optional[Tuple[float, float]]:
        """
        Find intersection point in the x-y plane.

        Both lines are parameterized as followed:
        lambda1 = (x - x1) / alpha1 = (y - y1) / beta1
        lambda2 = (x - x2) / alpha2 = (y - y2) / beta2

        By solving the equations for lambda1 and lambda 2 we can find the intersection.

        If an intersection is found, returns lamda1 and lambda2 for wich:
        alpha1*lambda1 + x1 = x = alpha2*lambda2 + x2
        beta1*lambda1 + y1 = y = b beta2*lambda2 + y2

        If no intersection is found, return None
        """
        x1 = self.point[0]
        alpha1 = self.direction[0]
        x2 = other.point[0]
        alpha2 = other.direction[0]

        y1 = self.point[1]
        beta1 = self.direction[1]
        y2 = other.point[1]
        beta2 = other.direction[1]

        try:
            top = y2 - y1 - (beta1 / alpha1) * (x2 - x1)
            bot = (beta1 * alpha2 / alpha1) - beta2
            la2 = top / bot
            la1 = (alpha2 * la2 + x2 - x1) / alpha1
        except ZeroDivisionError:
            return None

        return (la1, la2)


def parse_line(data: str) -> Line:
    """
    Parse a line of the input format into a Line object
    """
    point, direction = data.split("@", maxsplit=2)

    x, y, z = [int(x) for x in point.split(",", maxsplit=3)]
    a, b, g = [int(x) for x in direction.split(",", maxsplit=3)]

    return Line(point=(x, y, z), direction=(a, b, g))


def find_intersects(lines: List[Line], limits: Tuple[int, int]) -> int:
    """
    Given a list of lines and a given search area, find how many lines
    intersect in the `future` and inside the search area
    """
    intersects = 0

    for idx1 in range(len(lines)):
        for idx2 in range(idx1 + 1, len(lines)):
            line1 = lines[idx1]
            line2 = lines[idx2]

            lambdas = line1.intersects(line2)

            if lambdas is None:
                # no intersection found
                continue

            if any(x <= 0 for x in lambdas):
                # If for any line the lambda values <= 0, the intersection
                # happened in the past and we do not need to count it.
                continue

            # Get the coordinates at the intersection point
            p1 = line1.get_point_at_lambda(lambdas[0])

            # If the intersection point lies within the search area,
            # increase the counter.
            if limits[0] <= p1[0] <= limits[1] and limits[0] <= p1[1] <= limits[1]:
                intersects += 1
    return intersects


def compute(data: str, limits: Tuple[int, int]) -> Optional[int]:
    """Compute result for puzzle input"""
    lines = [parse_line(x) for x in data.splitlines()]

    return find_intersects(lines, limits)


def main():
    """Run puzzle input"""
    with open("day24_input.txt", "r") as f:
        data = f.read()

    limits = (200000000000000, 400000000000000)
    result = compute(data, limits)
    print(f"{result=}")


if __name__ == "__main__":
    main()

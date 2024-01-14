"""
collection of utility functions that seem to be helpful in multiple tasks
"""

import re
from enum import Enum


def get_integers_from_line(line: str) -> list[int]:
    """ Returns a list of integers present in the provided string """
    int_re = r"[-\d]+"
    return [int(x) for x in re.findall(int_re, line)]


def get_numbers_from_line(line: str) -> list[str]:
    """
    Returns a list of numbers (as string) present in the provided string
    """
    int_re = r"[-\d]+"
    return [x for x in re.findall(int_re, line)]


class Offsets(Enum):
    """
    Offsets in coords to go a direction in the grid.

    (delta_row, delta_col)
    """

    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

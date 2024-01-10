"""
collection of utility functions that seem to be helpful in multiple tasks
"""

import re


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

""" Advent of Code 2023 day 8 """

from dataclasses import dataclass
import re

INPUT1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
EXPECTED1 = 2

INPUT2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
EXPECTED2 = 6


def test_case1():
    """ Test case for example 1 part 1 """
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """ Test case for example 2 part 1 """
    assert compute(INPUT2) == EXPECTED2


@dataclass
class Node:
    """ Representation of a network node"""
    name: str
    l: str
    r: str

    @property
    def is_end(self):
        return self.name == "ZZZ"

    def get_next_nodes(self, direction: str):
        match direction.upper():
            case "L":
                result = self.l
            case "R":
                result = self.r
            case _:
                raise ValueError(
                    f"Incorrect direction '{direction}' provided."
                    )

        return result


def read_node_from_line(line: str) -> Node:
    """ Create node from input line """
    re_node = r"[A-Z]{3}"

    match = re.findall(re_node, line)

    if len(match) != 3:
        raise ValueError(f"Cannot parse node from {line}")

    return Node(match[0], match[1], match[2])


def count_steps_to_end(nodes: dict[str, Node], steps: str) -> int:
    node = nodes["AAA"]
    n_steps = 0

    while not node.is_end:
        next_node = node.get_next_nodes(steps[n_steps % len(steps)])
        node = nodes[next_node]
        n_steps += 1

    return n_steps


def compute(data: str) -> int:
    """ Compute the result for part 1 """
    re_steps = r"^[LR]+$"
    nodes: dict[str, Node] = {}

    for line in data.splitlines():
        if not line.strip():
            continue
        elif re.match(re_steps, line):
            steps = line
        else:
            node = read_node_from_line(line)
            nodes[node.name] = node

    return count_steps_to_end(nodes, steps)


def main():
    """ Runnning puzzle input """
    with open("day8_input.txt", "r") as f:
        data = f.read()

    result = compute(data)

    print(f"{result=}")


if __name__ == '__main__':
    main()

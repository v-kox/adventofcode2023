""" Advent of Code 2023 day 8 """

import math
import re
from dataclasses import dataclass

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

INPUT3 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
EXPECTED3 = 6


def test_case1():
    """ Test case for example 1 part 1 """
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """ Test case for example 2 part 1 """
    assert compute(INPUT2) == EXPECTED2


def test_case3():
    """ Test case for example part 2"""
    assert compute2(INPUT3) == EXPECTED3


@dataclass
class Node:
    """ Representation of a network node"""
    name: str
    l: str
    r: str

    @property
    def is_end(self) -> bool:
        """ Check if current node is end node"""
        return self.name == "ZZZ"

    @property
    def is_start_ghost(self) -> bool:
        """ Check if current node is a ghost start node """
        return self.name[-1] == "A"

    @property
    def is_end_ghost(self) -> bool:
        """ Check if current node is a ghost end node """
        return self.name[-1] == "Z"

    def get_next_nodes(self, direction: str):
        """
        Return the name of the next node based on
        on the given direction
        """
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
    re_node = r"\w{3}"

    match = re.findall(re_node, line)

    if len(match) != 3:
        raise ValueError(f"Cannot parse node from {line}")

    return Node(match[0], match[1], match[2])


def count_steps_to_end(nodes: dict[str, Node], steps: str) -> int:
    """ Count steps needed to go to end node """
    node = nodes["AAA"]
    n_steps = 0

    while not node.is_end:
        next_node = node.get_next_nodes(steps[n_steps % len(steps)])
        node = nodes[next_node]
        n_steps += 1

    return n_steps


def _count_step_1node_ghost(node: Node, nodes: dict[str, Node], steps) -> int:
    """ Count how many steps are required to reach a (ghost) end node """
    n_steps = 0

    while not node.is_end_ghost:
        next_node = node.get_next_nodes(steps[n_steps % len(steps)])
        node = nodes[next_node]
        n_steps += 1

    return n_steps


def count_steps_ghost(nodes: dict[str, Node], steps):
    """
    Returns the number of steps required to reach an end node
    simultaneously for all starting nodes.

    This happens by determining for each start node how many steps it
    takes to reach an end node and then calculating the least common
    multiplier (lcm). (paths loop in input.)
    """
    start_nodes = [node for node in nodes.values() if node.is_start_ghost]
    n_steps_to_end = [
        _count_step_1node_ghost(node, nodes, steps)
        for node in start_nodes
        ]
    return math.lcm(*n_steps_to_end)


def read_input(data: str) -> tuple[dict[str, Node], str]:
    """ Read steps and nodes from input data"""
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

    return nodes, steps


def compute(data: str) -> int:
    """ Compute the result for part 1 """
    nodes, steps = read_input(data)

    return count_steps_to_end(nodes, steps)


def compute2(data: str) -> int:
    """ Compute the result for part 2 """
    nodes, steps = read_input(data)

    return count_steps_ghost(nodes, steps)


def main():
    """ Runnning puzzle input """
    with open("day8_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    result2 = compute2(data)

    print(f"{result=}")
    print(f"{result2=}")


if __name__ == '__main__':
    main()

import random
from collections import defaultdict
from copy import deepcopy
from typing import Dict
from typing import List

INPUT1 = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""


def test_case1():
    assert compute(INPUT1) == 54


def parse_data(data: str) -> dict[str, List[str]]:
    components = defaultdict(list)
    for line in data.splitlines():
        c1, other_comp = line.split(":", maxsplit=2)

        for c2 in other_comp.strip().split(" "):
            components[c1].append(c2)
            components[c2].append(c1)
    return components


def karger_algo(graph: Dict[str, List[str]], n_edge: int):
    """
    This is a basic implementation of Karger's Algorithm, slightly
    modified to ensure that the 2 end graphs are connected by exactly 3
    edges.

    The idea is to contact 2 connected nodes together (and updating the edges)
    until only 2 nodes remain. These 2 nodes then represent the split graph

    More info:
    https://en.wikipedia.org/wiki/Karger%27s_algorithm
    """
    while True:
        # create a copy of the graph, since it isn't guaranteed to
        # find the correct solution on the first iteration.
        iter_graph = deepcopy(graph)

        while len(iter_graph) > 2:
            # randomly select 2 nodes that have an edge to contract
            n1 = random.choice(sorted(iter_graph))
            n2 = random.choice(iter_graph[n1])

            # create new joined node
            new_node = ",".join([n1, n2])

            # create new edges
            #
            # Note: by using `pop` we remove `n1` and `n2` from the graph
            # Note 2: if both have an edge to the same node (e.g. both nodes A and B
            # are connected to node C), the edge needs to be added twice!
            new_neighours = [
                x for x in iter_graph.pop(n1) + iter_graph.pop(n2) if x not in (n1, n2)
            ]

            for n in new_neighours:
                # For all the neighbours, remove the connection to the old nodes
                # and add a connection to the newly contracted node.
                iter_graph[n] = [x for x in iter_graph[n] if x not in (n1, n2)]
                iter_graph[n].append(new_node)

            # add neighbours for newly contracted node
            iter_graph[new_node] = new_neighours

        # If the number of edhes that remain equal `n_edge`
        # we found a cut that satisfies the requirements
        if max(len(x) for x in iter_graph.values()) == n_edge:
            # Since the graph consists of only 2 nodes, we can count the number of
            # riginal nodes by splitting the name on `,`. The puzzle result is then
            # the multiplication of both these numbers
            n_nodes1, n_nodes2 = [len(x.split(",")) for x in iter_graph]
            return n_nodes1 * n_nodes2

    # this is to make mypy happy
    raise AssertionError("Unreachable code")


def compute(data: str) -> int:
    """compute result"""
    graph = parse_data(data)
    return karger_algo(graph, 3)


def main():
    """Run puzzle input"""
    with open("day25_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    print(f"{result=}")


if __name__ == "__main__":
    main()

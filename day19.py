import re
from typing import Callable, NamedTuple, Optional

from utils import get_integers_from_line

INPUT1 = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
EXPECTED1 = 19114


def test_parse_part_string():
    """Test parsing of Part string"""
    assert get_part_from_string("{x=0,m=1,a=2,s=3}") == Part(0, 1, 2, 3)
    assert get_part_from_string("{x=1000,m=234,a=9876,s=55555}") == Part(
        1000, 234, 9876, 55555
    )


def test_parse_rule_string():
    """Test parsing of rule string"""
    rule_str1 = "s>2770:qs"
    rule_str2 = "R"
    rule_str3 = "hdj"

    assert get_rule_from_string(rule_str1) == Rule(test="s>2770", result="qs")
    assert get_rule_from_string(rule_str2) == Rule(result="R")
    assert get_rule_from_string(rule_str3) == Rule(result="hdj")


def test_parse_workflow():
    """Test parsing of workflow string"""
    wf_string = "hdj{m>838:A,pv}"

    name, rules = get_workflow_from_string(wf_string)

    assert name == "hdj"
    assert len(rules) == 2
    assert rules[0] == Rule(test="m>838", result="A")
    assert rules[1] == Rule(result="pv")


def test_apply_valid_rule_to_part():
    """Test that a valid rule returns True"""
    r1 = Rule(test="x>1", result="A")
    r2 = Rule(test="m<9001", result="A")
    r3 = Rule(test="a=5000", result="A")
    r4 = Rule(result="R")

    p = Part(x=1000, m=0, a=5000, s=10000)

    assert r1.is_valid(p)
    assert r2.is_valid(p)
    assert r3.is_valid(p)
    assert r4.is_valid(p)


def test_apply_invalid_rule_to_part():
    """Test that an invalid rule returns False"""
    r1 = Rule(test="x>10000", result="A")
    r2 = Rule(test="m<0", result="A")
    r3 = Rule(test="a=5000", result="A")

    p = Part(x=0, m=10000, a=5001, s=10000)

    assert not r1.is_valid(p)
    assert not r2.is_valid(p)
    assert not r3.is_valid(p)


def test_case1():
    """Test case example part 1"""
    assert compute(INPUT1) == EXPECTED1


class Part(NamedTuple):
    """Wrappaer class to represent a Part in the puzzle"""

    x: int
    m: int
    a: int
    s: int


class Rule(NamedTuple):
    """Wrapper class to represent the rules in the puzzle"""

    result: str
    test: Optional[str] = None

    @property
    def _test_param(self):
        """Get the Part parameter that needs to to fullfill the Rule"""
        if self.test is None:
            return ""
        else:
            return self.test[0]

    @property
    def _op_str(self) -> str:
        """Get the comparison operator"""
        return "" if self.test is None else self.test[1]

    @property
    def _test_value(self) -> int:
        """Get the test value that needs to be compared to the part"""
        if self.test is None:
            return 0

        return get_integers_from_line(self.test)[0]

    @property
    def _test_func(self) -> Callable[[int], bool]:
        """
        Based on the operator string and test value, return the function
        that needs to be applied to the Part
        """
        match self._op_str:
            case "<":
                return lambda x: x < self._test_value
            case ">":
                return lambda x: x > self._test_value
            case "=":
                return lambda x: x == self._test_value

        raise NotImplementedError(f"Cannot use operator: {self._op_str}")

    def is_valid(self, p: Part) -> bool:
        """Check if Part p fullfills the current Rule"""
        if self.test is None:
            return True

        return self._test_func(getattr(p, self._test_param))


# helper type
Workflow = dict[str, list[Rule]]


def get_rule_from_string(rule: str) -> Rule:
    """Read Rule information from input string"""
    re_rule = re.compile(r"([a-z][<>=]\d+)?:?(\w+)")

    re_match = re_rule.match(rule)

    if re_match is None:
        raise ValueError(f"Cannot parse rule string: {rule}")

    return Rule(test=re_match.group(1), result=re_match.group(2))


def get_part_from_string(part: str) -> Part:
    """Parse part information from input string"""
    re_part = re.compile(r"([a-z])=(\d+)")
    data = {key: int(val) for key, val in re_part.findall(part)}

    if len(data) == 0:
        raise ValueError(f"Cannot parse part string: {part}")
    return Part(**data)


def get_workflow_from_string(wf: str) -> tuple[str, list[Rule]]:
    """Parse a workflow line into it's valid data"""
    re_wf = re.compile(r"(\w+)\{(.+)\}")

    re_match = re_wf.match(wf)

    if re_match is None:
        raise ValueError(f"Cannot parse workflow string: {wf}")

    wf_name = re_match.group(1)
    wf_rules = [get_rule_from_string(s) for s in re_match.group(2).split(",")]

    return wf_name, wf_rules


def get_result_from_workflow(part: Part, wf: list[Rule]):
    """Get the result from running the workflow on a part"""
    results = [rule.result for rule in wf if rule.is_valid(part)]

    return results[0]


def is_part_accepted(part: Part, wfs: Workflow, start_wf: str = "in") -> bool:
    """Check if a part is accepted"""
    result = get_result_from_workflow(part, wfs[start_wf])

    if result == "A":
        return True
    elif result == "R":
        return False
    else:
        # If no final result from wf, run the next workflow
        return is_part_accepted(part, wfs, result)


def parse_data(data: str) -> tuple[Workflow, list[Part]]:
    """
    Parse the input data format into a workflow dict and a list of Parts
    """
    wfs: Workflow = {}
    parts: list[Part] = []

    is_wf = True

    for line in data.splitlines():
        if not line.strip():
            # If we encounter an empty line. We go from workflows to parts
            is_wf = False
            continue

        if is_wf:
            wf_name, wf_rules = get_workflow_from_string(line)
            wfs[wf_name] = wf_rules
        else:
            parts.append(get_part_from_string(line))

    return wfs, parts


def compute(data: str) -> int:
    """Compute the puzzle output"""
    wfs, parts = parse_data(data)

    accepted_parts = [p for p in parts if is_part_accepted(p, wfs)]

    return sum(p.x + p.s + p.m + p.a for p in accepted_parts)


def main():
    """Run puzzle input"""
    with open("day19_input.txt", "r") as f:
        data = f.read()

    result = compute(data)

    print(f"{result=}")


if __name__ == "__main__":
    main()

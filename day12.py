from utils import get_integers_from_line
from functools import lru_cache
INPUT0 = """\
???.### 1,1,3
"""
EXPECTED0 = 1


INPUT1 = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
EXPECTED1 = 21
EXPECTED2 = 525152


def test_case0():
    """Test case 1 simple line"""
    assert compute(INPUT0) == EXPECTED0


def test_case1():
    """Test case provided example"""
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    """Test case provided example part 2"""
    assert compute2(INPUT1) == EXPECTED2


# For part 2 add cache to function. To avoid recalculating the same sequence.
# Also changed groups parameter from list to tuple, since list is mutable and
# thus not hashable for caching
@lru_cache(maxsize=None)
def count_arrangements(line: str, groups: tuple[int]) -> int:
    """
    Count the max possible arrangements of
    """
    # No more groups of broken springs.
    # If no more `#` in line, then arrangement is valid, else not valid
    if not groups:
        return 0 if "#" in line else 1

    # Line is empty or only fixed springs.
    # We still need broken springs. So invalid arrangement
    if not line or all((c == "." for c in line)):
        return 0

    # If there are more groups than springs left, or
    # the number of broken springs for the first group
    # is larger than the remaining number of springs. Invalid arrangement.
    if len(line) < len(groups) or len(line) < groups[0]:
        return 0

    match line[0]:
        case ".":
            # If fixed spring, continue with next character
            return count_arrangements(line[1:], groups)
        case "?":
            # If unknown check both possibilities
            return count_arrangements("#" + line[1:], groups) + count_arrangements(
                "." + line[1:], groups
            )
        case "#":
            # If broken spring:
            #   1. If fixed spring in the next `n` characters invalid arrangement
            #   2. If line length equal to group size. Check if valid arrangement
            #   3. If line length > group size. Check first element after group.
            #     3.1. If broken spring, invalid arrangement (group size too large)
            #     3.2. If fixed spring continue processing rest of the line
            #     3.3. If unknown, continue processing assuming fixed spring.
            if "." in line[: groups[0]]:
                return 0
            elif len(line) == groups[0]:
                return count_arrangements(line[groups[0] :], groups[1:])
            else:
                match line[groups[0]]:
                    case "#":
                        return 0
                    case ".":
                        return count_arrangements(line[groups[0] + 1 :], groups[1:])
                    case "?":
                        return count_arrangements(
                            "." + line[groups[0] + 1 :], groups[1:]
                        )

    raise NotImplementedError("This code should not be reachable")


def compute(data: str) -> int:
    total = 0
    for line in data.splitlines():
        format1, format2 = line.split()

        # Get groupings of broken springs
        groups = tuple(get_integers_from_line(format2))

        total += count_arrangements(format1, groups)

    return total


def compute2(data: str) -> int:
    total = 0
    for line in data.splitlines():
        format1, format2 = line.split()

        line = "?".join(5*[format1])

        groups = tuple(5*get_integers_from_line(format2))

        # Get groupings of broken springs
        total += count_arrangements(line, groups)

    return total


def main():
    """Runnning puzzle input"""
    with open("day12_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    result2 = compute2(data)
    print(f"{result=}")
    print(f"{result2=}")


if __name__ == "__main__":
    main()

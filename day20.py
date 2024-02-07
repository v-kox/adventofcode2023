import re

from day20_utils import HIGH
from day20_utils import Broadcast
from day20_utils import Button
from day20_utils import Conjunction
from day20_utils import FlipFlop
from day20_utils import Module
from day20_utils import Pulse
from day20_utils import Untyped

INPUT1 = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
EXPEXTED1 = 32000000

INPUT2 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""
EXPECTED2 = 11687500


def test_case1():
    """Test example 1 part 1"""
    assert compute(INPUT1) == EXPEXTED1


def test_case2():
    """Test example 2 part 1"""
    assert compute(INPUT2) == EXPECTED2


def _read_line(line: str):
    """Read module information from a single line"""
    re_module = re.compile(r"(&|%)?([a-zA-Z]+)")
    mod_str, n_str = line.split("->")

    re_match = re_module.match(mod_str.strip())
    neighbours = [x.strip() for x in n_str.split(",")]
    if re_match is None:
        raise ValueError(f"Could not parse line: {line}")

    match re_match.group(1):
        case "%":
            return FlipFlop(re_match.group(2), neighbours)
        case "&":
            return Conjunction(re_match.group(2), neighbours, [])
        case None:
            return Broadcast(neighbours)
        case _:
            raise ValueError(f"Don't know what to do with {re_match.group(1)}")


def modules_state(modules: dict[str, Module]) -> dict[str, str]:
    """Get the state of all modules from the id field"""
    return {key: value.id for key, value in modules.items()}


def parse_modules(data: str) -> dict[str, Module]:
    """parse input data into dictionary of modules"""
    modules = {}
    for line in data.splitlines():
        module = _read_line(line)
        modules[module.name] = module

    # Bad function to get sources for conjuntion modules
    for n, m in modules.items():
        if not isinstance(m, Conjunction):
            continue

        sources = []
        for m2 in modules.values():
            if n in m2.neighbours:
                sources.append(m2.name)
        modules[n] = Conjunction(m.name, m.neighbours, sources)
    return modules


def compute_pulses(
    modules: dict[str, Module],
    button: Button,
    max_loops: int,
) -> tuple[int, int]:
    """Compute low and high pulse count"""
    # start state of the modules
    start_state = modules_state(modules)

    # start queue of pulses
    pulse_queue: list[Pulse] = []
    pulse_queue.append(button.push())

    # start count for high and low pulses
    n_low = 0
    n_high = 0

    # bool variable to check if a loop is found
    loop_found = False

    # Loop until we reacht the loop limit
    while button.n_push <= max_loops:
        if not pulse_queue:
            if modules_state(modules) == start_state:
                # If current state == starting state, found a loop.
                # break from the calculations.
                loop_found = True
                break

            # Queue is empty, push the button
            pulse = button.push()
            pulse_queue.append(pulse)
        else:
            # get first pulse from the queue
            pulse = pulse_queue.pop(0)

            # increase relevant counter
            if pulse.level == HIGH:
                n_high += 1
            else:
                n_low += 1

            # get new puleses from the destination module and add to queue
            new_pulses = modules.get(
                pulse.dest,
                Untyped(pulse.dest),
            ).receive_pulse(pulse)
            pulse_queue += new_pulses

    if loop_found:
        # If a loop is found, calculate number of low and high pulses totally
        n_loops = max_loops // button.n_push
        n_rem_buttons = max_loops % button.n_push

        n_low *= n_loops
        n_high *= n_loops

        # Recursively call function with remaining number of loops
        n_low2, n_high2 = compute_pulses(modules, Button(), n_rem_buttons)
        n_low += n_low2
        n_high += n_high2

    return n_low, n_high


def compute(data: str) -> int:
    modules = parse_modules(data)

    # Create button. Push button to start sequence
    button = Button()

    n_low, n_high = compute_pulses(modules, button, 1000)

    return n_high * n_low


def main():
    """Run puzzle input"""
    with open("day20_input.txt", "r") as f:
        data = f.read()

    result = compute(data)

    print(f"{result=}")


if __name__ == "__main__":
    main()

from abc import ABC
from abc import abstractmethod
from typing import NamedTuple

LOW = 0
HIGH = 1


class Pulse(NamedTuple):
    """representation of a Pulse"""

    source: str
    dest: str
    level: int


class Module(ABC):
    """abstract representation of a Module"""

    name: str
    symbol: str
    neighbours: list[str]

    @property
    @abstractmethod
    def id(self) -> str: ...

    @abstractmethod
    def receive_pulse(self, pulse: Pulse) -> list[Pulse]: ...


class Button(Module):
    """
    Sends a low pulse to the broadcast
    """

    symbol = "button"
    name = "button"
    id = "button"
    neighbours = ["broadcaster"]
    n_push = 0

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        return []

    def push(self):
        """Push the button"""
        self.n_push += 1
        return Pulse(self.name, "broadcaster", LOW)


class Broadcast(Module):
    """
    Broadcast:
    Sends the same pulse to all it's neighbours
    """

    symbol = "broadcaster"
    name = "broadcaster"
    id = "broadcaster"

    def __init__(self, neighbours: list[str]) -> None:
        self.neighbours = neighbours

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        return [Pulse(self.name, x, pulse.level) for x in self.neighbours]


class FlipFlop(Module):
    """
    FliFlop:
    sends pulse depending on it's on state
    """

    symbol = "%"

    def __init__(self, name, neighbours) -> None:
        self.name = name
        self.neighbours = neighbours

        # flipflop module starts in off state
        self.on = False

    @property
    def id(self) -> str:
        state = "on" if self.on else "off"
        return f"{self.symbol}_{self.name}_{state}"

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        if pulse.level == HIGH:
            return []
        else:
            # flip on state
            self.on = not self.on
            pulse_level = HIGH if self.on else LOW
            return [Pulse(self.name, x, pulse_level) for x in self.neighbours]


class Conjunction(Module):
    """
    Conjunction module:
    sends pulse depending on the previousle received pules from it's inputs"""

    symbol = "&"

    def __init__(self, name: str, neighbours: list[str], sources: list[str]) -> None:
        self.name = name
        self.neighbours = neighbours

        self.sources = sources
        self.prev_pulse: dict[str, int] = {x: LOW for x in sources}

    @property
    def id(self) -> str:
        # String of previous incoming pulses
        prev_str = "_".join([f"{k}:{v}" for k, v in self.prev_pulse.items()])

        return f"{self.symbol}_{self.name}_{prev_str}"

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        self.prev_pulse[pulse.source] = pulse.level

        level = LOW if all(x == HIGH for x in self.prev_pulse.values()) else HIGH
        # breakpoint()
        return [Pulse(self.name, x, level) for x in self.neighbours]


class Untyped(Module):
    """Untyped module. Only receives, doesn't send pulses"""

    symbol = "untyped"
    neighbours = []

    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def id(self) -> str:
        return f"{self.symbol}_{self.name}"

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        return []

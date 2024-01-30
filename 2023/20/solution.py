import abc
from dataclasses import dataclass


Pulse = tuple[int, bool]  # False = Low, True = High


@abstract
@dataclass
class Module(abc.ABC):
    inputs: tuple[Module]
    outputs: tuple[Module]

    @abc.abstractmethod
    def process(self, *inputs: Pulse) -> tuple[Pulse]:
        pass


@dataclass
class Button(Module):
    def process(self, *inputs: Pulse) -> tuple[Pulse]:
        return (False,)


@dataclass
class Broadcaster(Module):
    def process(self, *inputs: Pulse) -> tuple[Pulse]:
        return tuple([inputs[0] for _ in self.outputs])


@dataclass
class FlipFlop(Module):
    is_on: bool = False

    def process(self, *inputs: Pulse) -> tuple[Pulse]:
        if len(inputs) > 1:
            raise ValueError(
                f'Inputs should be of size 1 for FlipFlop: received {inputs}'
            )
        priority, pulse = inputs[0]
        if pulse:
            return []

        self.is_on = not self.is_on
        return tuple([self.is_on for _ in self.outputs])


@dataclass
class Conjunction(Module):

    def __init__(self, inputs: tuple[Module], outputs: tuple[Module]):
        self.inputs = inputs
        self.outputs = outputs
        self.memory = tuple([False for _ in outputs])

    def process(self, *inputs: Pulse) -> tuple[Pulse]:
        self.memory
def load(filename: str) -> list[Module]

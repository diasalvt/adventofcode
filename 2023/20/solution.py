import abc
from dataclasses import dataclass


Pulse = bool  # False = Low, True = High


def encapsulate_pulse(process_function):
    def f(*args, **kwargs):
        results = process_function(*args, **kwargs)
        return tuple([(elem[0] + 1, elem[1]) for elem in results])
    return f


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
    @encapsulate_pulse
    def process(self, *inputs: Pulse) -> tuple[Pulse]:
        return (False,)


@dataclass
class Broadcaster(Module):
    @encapsulate_pulse
    def process(self, *inputs: Pulse) -> tuple[Pulse]:
        return tuple([inputs[0] for _ in self.outputs])


@dataclass
class FlipFlop(Module):
    is_on: bool = False

    @encapsulate_pulse
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

    @encapsulate_pulse
    def process(self, *inputs: Pulse) -> tuple[Pulse]:
        self.memory


def 
def load(filename: str) -> list[Module]

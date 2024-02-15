import abc
from dataclasses import dataclass
from typing import Optional


Pulse = tuple[int, bool]  # False = Low, True = High


def encapsulate_pulse(process_function):
    def f(self, *args, **kwargs):
        pulse = process_function(self, *args, **kwargs)
        if pulse is None:
            return []
        return [(pulse, output) for output in self.outputs]
    return f


@dataclass
class Module(abc.ABC):
    outputs: tuple

    @abc.abstractmethod
    def process(self, inp: Pulse) -> Optional[Pulse]:
        pass


@dataclass
class Button(Module):
    @encapsulate_pulse
    def process(self) -> Optional[Pulse]:
        return False


def test_button():
    b = Button(())
    assert not Button((b,)).process()[0] == (1, False, b)


@dataclass
class Broadcaster(Module):
    @encapsulate_pulse
    def process(self, inp: Pulse) -> Optional[Pulse]:
        return inp


b = Button(())
print(Broadcaster((b,)).process((1, True)))


def test_broadcaster():
    b = Button(())
    assert Broadcaster((b,)).process((1, True))[0] == (2, True, b)


@dataclass
class FlipFlop(Module):
    is_on: bool = False

    @encapsulate_pulse
    def process(self, inp: Pulse) -> Optional[Pulse]:
        priority, pulse = inp
        if pulse:
            return None

        self.is_on = not self.is_on
        return (priority, self.is_on)


@dataclass
class Conjunction(Module):

    def __init__(self, outputs: tuple[Module]):
        self.outputs = outputs
        self.memory = tuple([False for _ in outputs])

    @encapsulate_pulse
    def process(self, inp: Pulse) -> Pulse:
        self.memory

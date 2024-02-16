import abc
from dataclasses import dataclass
from typing import Optional
from collections import defaultdict


Pulse = bool  # False = Low, True = High


@dataclass
class Module(abc.ABC):
    outputs: tuple[str]

    @abc.abstractmethod
    def process(self, inp: Pulse, from_module: str) -> Optional[Pulse]:
        pass


@dataclass
class Button(Module):
    def process(self, inp: Pulse, from_module: str) -> Optional[Pulse]:
        return False


@dataclass
class Broadcaster(Module):
    def process(self, inp: Pulse, from_module: str) -> Optional[Pulse]:
        return inp


@dataclass
class FlipFlop(Module):
    is_on: bool = False

    def process(self, inp: Pulse, from_module: str) -> Optional[Pulse]:
        if inp:
            return None

        self.is_on = not self.is_on
        return self.is_on


@dataclass
class Conjunction(Module):
    memory = defaultdict(bool)

    def process(self, inp: Pulse, from_module: str) -> Pulse:
        self.memory[from_module] = inp
        return all(self.memory.values())


Event = tuple[int, Pulse, Module, Module]


def load(filename: str) -> dict[str, Module]:

    def row_to_module(s: str) -> tuple[str, Module]:
        inp, outputs = s.strip().split(' -> ')
        outputs = tuple(outputs.split(', '))

        match inp[0]:
            case 'b':
                return (inp, Broadcaster(outputs))
            case '%':
                return (inp[1:], FlipFlop(outputs))
            case '&':
                return (inp[1:], Conjunction(outputs))
            case _:
                raise ValueError(f'{inp=} is not valid.')

    with open(filename) as f:
        return {
            module_name: module
            for module_name, module in map(row_to_module, f)
        }


test = load('test.txt')
test2 = load('test2.txt')
print(test)


def run(modules: dict[str, Module], press_button: int = 1) -> list[Module]:
    b = Button(('broadcaster',))
    modules['button'] = b

    def exec_event(event: Event, modules: dict[str, Module]) -> list[Event]:
        priority, pulse_in, sender, receiver = event
        if receiver not in modules:
            return modules, []

        pulse_out = modules[receiver].process(pulse_in, sender)
        return modules, [
            (priority + 1, pulse_out, receiver, output)
            for output in modules[receiver].outputs
            if pulse_out is not None
        ]

    pulse_processed = []
    for i in range(press_button):
        queue: list[Event] = [(0, False, 'void', 'button')]

        while queue:
            event = queue.pop(0)
            print(event)
            modules, new_events = exec_event(event, modules)
            pulse_processed.extend([e for _, e, _, _ in new_events])
            queue.extend(new_events)
            queue = sorted(queue)

    return pulse_processed

print(sum(run(test, 1)))

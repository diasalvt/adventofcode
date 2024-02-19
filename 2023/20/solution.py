import abc
from dataclasses import dataclass, field
from typing import Optional, Self
from collections import Counter, defaultdict
from itertools import pairwise
from math import lcm


Pulse = bool  # False = Low, True = High


@dataclass
class Module(abc.ABC):
    outputs: list[str]
    inputs: list[str] = field(default_factory=list)

    @abc.abstractmethod
    def process(self, inp: Pulse, from_module: str) -> Optional[Pulse]:
        pass

    def update_inputs(self, input_name: str) -> Self:
        self.inputs.append(input_name)
        return self


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
    memory: dict[str, bool] = field(default_factory=dict)

    def update_inputs(self, input_name: str) -> Self:
        self.inputs.append(input_name)
        self.memory[input_name] = False
        return self

    def process(self, inp: Pulse, from_module: str) -> Pulse:
        self.memory[from_module] = inp
        return not all(self.memory.values())


Event = tuple[int, Pulse, Module, Module]


def load(filename: str) -> dict[str, Module]:

    def parse(s: str) -> tuple[str, tuple[str]]:
        inp, outputs = s.strip().split(' -> ')
        outputs = tuple(outputs.split(', '))
        return inp, outputs

    def row_to_module(s: str) -> tuple[str, Module]:
        inp, outputs = parse(s)

        match inp[0]:
            case 'b':
                return (inp, Broadcaster(outputs))
            case '%':
                return (inp[1:], FlipFlop(outputs))
            case '&':
                return (inp[1:], Conjunction(outputs))
            case _:
                raise ValueError(f'{inp=} is not valid.')

    rows = list(open(filename))
    d = {
        module_name: module
        for module_name, module in map(row_to_module, rows)
    }

    for inp, outputs in map(parse, rows):
        for out in outputs:
            if out in d:
                if inp[0] in ['%', '&']:
                    d[out].update_inputs(inp[1:])
                else:
                    d[out].update_inputs(inp)

    return d


def run(modules: dict[str, Module], press_button: int = 1) -> list[Module]:
    b = Button(('broadcaster',))
    modules['button'] = b
    pulse_counter = Counter()

    def exec_event(event: Event, modules: dict[str, Module]) -> list[Event]:
        priority, _, pulse_in, sender, receiver = event
        if receiver not in modules:
            return modules, []

        pulse_out = modules[receiver].process(pulse_in, sender)
        return modules, [
            (priority + 1, i, pulse_out, receiver, output)
            for i, output in enumerate(modules[receiver].outputs)
            if pulse_out is not None
        ]

    modules_to_watch = ['sk', 'qz', 'sv', 'dr']
    save = defaultdict(list)
    for i in range(1, press_button + 1):
        queue: list[Event] = [(0, 0, False, 'void', 'button')]

        while queue:
            event = queue.pop(0)
            modules, new_events = exec_event(event, modules)
            if event[-1] in modules_to_watch:
                if all(modules[event[-1]].memory.values()):
                    save[event[-1]].append(i)
            pulse_counter.update([e for _, _, e, _, _ in new_events])
            queue.extend(new_events)
            queue = sorted(queue)

    diff = {
        k: [b - a for a, b in pairwise(v)][0]
        for k, v in save.items()
    }
    return pulse_counter, lcm(*diff.values())


data = load('input.txt')
# data = load('bug.txt')
part1, part2 = run(data, 1000)
print(part1[False] * part1[True])

part1, part2 = run(data, 10000)
print(part2)

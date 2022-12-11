from collections import Counter
from dataclasses import dataclass
from typing import Callable, Self
import re
from operator import add, mul


def parse_file(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().split('\n\n')


raw_monkey_settings = parse_file('input.txt')
raw_monkey_settings_test = parse_file('test.txt')

ops = {
    '+': add,
    '*': mul
}


@dataclass
class NModulo:
    modulos: dict

    @classmethod
    def from_int(cls, val: int) -> Self:
        return cls({mod: val % mod for mod in [2, 3, 5, 7, 11, 13, 17, 19]})

    def __add__(self, other: int) -> Self:
        return {k: (v + other) % k for k, v in self.modulos}

    def __mul__(self, other: int) -> Self:
        return {k: (v * other) % k for k, v in self.modulos}


@dataclass
class Monkey:
    items: list[int]
    op: Callable[int, int]
    picker: Callable[int, int]  # from item value to monkey number

    @classmethod
    def from_str(cls, text: str) -> 'Monkey':
        number, starting, op, *test = text.splitlines()
        starting = list(map(int, re.findall(r'\d+', starting)))
        match op.split(': new = ')[1].split():
            case ['old', operator, 'old']:
                def op(x): return ops[operator](x, x)
            case ['old', operator, b]:
                def op(x): return ops[operator](x, int(b))

        test, iftrue, iffalse = [int(s.split()[-1]) for s in test]
        def picker(x): return iftrue if (x % test) == 0 else iffalse

        return cls(starting, op, picker)

    def __repr__(self):
        return f'Monkey({self.items=})'


def game(
    raw_settings: str, nb_rounds: int = 20, divide_worry: int = 3,
    monkey_type=Monkey
) -> list:
    monkeys = [monkey_type.from_str(s) for s in raw_settings]
    monkeys_inspection_counter = Counter()

    for _ in range(nb_rounds):
        for i, monkey in enumerate(monkeys):
            for item in monkey.items:
                new_level = monkey.op(item) // divide_worry
                monkeys[monkey.picker(new_level)].items.append(new_level)
                monkeys_inspection_counter[i] += 1
            monkey.items = []

    return monkeys, monkeys_inspection_counter


_, counter = game(raw_monkey_settings, 20)
(_, v1), (_, v2) = counter.most_common(2)
print(f'Result {v1 * v2=}')


@dataclass
class NModulo:
    modulos: dict

    @classmethod
    def from_int(cls, val: int) -> Self:
        return cls({mod: val % mod for mod in [2, 3, 5, 7, 11, 13, 17, 19, 23]})

    def __add__(self, other: int) -> Self:
        return self.__class__({k: (v + other) % k for k, v in self.modulos.items()})

    def __mul__(self, other: int) -> Self:
        match other:
            case int(a):
                return self.__class__({k: (v * a) % k for k, v in self.modulos.items()})
            case _:
                return self.__class__({k: (v * other.modulos[k]) % k for k, v in self.modulos.items()})

    def __mod__(self, other: int) -> int:
        return self.modulos[other]

    def __floordiv__(self, other: int) -> Self:
        return self


@dataclass
class ModMonkey:
    items: list[NModulo]
    op: Callable[NModulo, int]
    picker: Callable[NModulo, int]  # from item value to monkey number

    @classmethod
    def from_str(cls, text: str) -> 'Monkey':
        number, starting, op, *test = text.splitlines()
        starting = list(map(NModulo.from_int,
                            map(int, re.findall(r'\d+', starting))))
        match op.split(': new = ')[1].split():
            case ['old', operator, 'old']:
                def op(x): return ops[operator](x, x)
            case ['old', operator, b]:
                def op(x): return ops[operator](x, int(b))

        test, iftrue, iffalse = [int(s.split()[-1]) for s in test]
        def picker(x): return iftrue if (x % test) == 0 else iffalse

        return cls(starting, op, picker)

    def __repr__(self):
        return f'Monkey({self.items=})'


res, counter = game(raw_monkey_settings, 10000, 1, ModMonkey)
(_, v1), (_, v2) = counter.most_common(2)
print(counter)
print(f'Result {v1 * v2=}')

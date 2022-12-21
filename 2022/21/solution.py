from typing import Self, Optional, Callable
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from tqdm import tqdm


_OPERATORS = {
    '*': lambda x, y: x * y,
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '/': lambda x, y: x // y,
}


@dataclass
class Op:
    inputs: list[str | int]
    op: Optional[Callable]
    output: str

    @classmethod
    def from_str(cls, s: str) -> Self:
        output, cmd = s.split(': ')
        match cmd.split(r' '):
            case [integer]:
                return cls([int(integer)], None, output)
            case [operand1, op, operand2]:
                return cls([operand1, operand2], _OPERATORS[op], output)
            case _:
                raise ValueError(f'{s} is not a valid Op')

    def compute(self, monkeys: dict['Op']) -> int:
        try:
            return self.value
        except AttributeError:
            match self.inputs:
                case [int(val)]:
                    self.value = val
                case [op1, op2]:
                    self.value = self.op(
                        monkeys[op1].compute(monkeys),
                        monkeys[op2].compute(monkeys)
                    )
            return self.value


def parse_file(filename: str) -> dict[Op]:
    with open(filename) as f:
        return {
            op.output: op
            for op in [Op.from_str(line) for line in f.read().splitlines()]
        }


def part_1(filename: str) -> int:
    monkeys = parse_file(filename)
    return monkeys['root'].compute(monkeys)


test = parse_file('test.txt')
print(part_1('test.txt'))
print(part_1('input.txt'))


def depending(monkey: str, monkeys: dict[Op]) -> set[str]:
    depending_monkey = set()
    next_depending_monkeys = {monkey}

    # Compute for each monkey who are the monkey depending on it
    monkey_dependance = defaultdict(list)
    for m, op in monkeys.items():
        if op.op is not None:
            m1, m2 = op.inputs
            monkey_dependance[m1].append(m)
            monkey_dependance[m2].append(m)

    while next_depending_monkeys:
        next_depending_monkeys = set(
            chain.from_iterable(
                monkey_dependance[m] for m in next_depending_monkeys
            )
        )
        depending_monkey |= next_depending_monkeys
    return depending_monkey


print(depending('humn', test))


def part_2(filename: str) -> int:
    monkeys = parse_file(filename)

    monkeys['root'].op = lambda x, y: x - y
    depend_on = {'humn'} | depending('humn', monkeys)

    def diff(humn_val: int) -> int:
        monkeys['humn'].inputs = [humn_val]
        result = monkeys['root'].compute(monkeys)

        for m in depend_on:
            try:
                delattr(monkeys[m], 'value')
            except AttributeError:
                pass
        return result

    high_pos = 4_518_000_000_000
    low_pos = 0
    _val1, _val2 = diff(low_pos), diff(high_pos)
    low_val, high_val = sorted([_val1, _val2])

    if _val1 < 0 and _val2 > 0:
        pos_greater_0 = high_pos
        pos_lower_0 = low_pos
    elif _val1 > 0 and _val2 < 0:
        pos_greater_0 = low_pos
        pos_lower_0 = high_pos
    else:
        raise ValueError("Range is too narrow and does not include positive and negative")

    while True:
        i = (pos_lower_0 + pos_greater_0) // 2

        print(pos_lower_0, pos_greater_0)
        res = diff(i)
        if res == 0:
            return i
        elif res < 0:
            pos_lower_0 = i
        else:
            pos_greater_0 = i

    return high_val


# print(part_2('test.txt'))
print(part_2('input.txt'))

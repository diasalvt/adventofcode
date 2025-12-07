from operator import mul, add
from functools import reduce
from itertools import takewhile
from typing import Iterable, Any


def load(filename: str) -> list[tuple[list[int], str]]:
    with open(filename) as f:
        lines = f.read().splitlines()

    *numbers, operators = lines
    numbers = [map(int, row.split()) for row in numbers]
    operators = operators.split()
    return list(zip(*numbers, operators))


commands = load('input.txt')

result = sum(
    reduce({'+': add, '*': mul}[op], numbers)
    for *numbers, op in commands
)
print(result)


def load_part_2(filename: str) -> list[tuple[list[int], str]]:
    with open(filename) as f:
        lines = f.read().splitlines()

    *numbers, operators = lines
    return list(zip(*numbers, operators))


commands = load_part_2('input.txt')


def tuple_str_to_int(t: tuple[str]) -> int | None:
    if all(t_i == ' ' for t_i in t):
        return None
    return int(''.join(t).replace(' ', ''))


def cut(it: Iterable, separator: Any = None) -> Iterable:
    it = iter(it)
    while t := tuple(takewhile(lambda x: x is not separator, it)):
        yield t
    

numbers = cut([tuple_str_to_int(line[:-1]) for line in commands])
operators = [line[-1] for line in commands if line[-1] != ' ']

print(
    sum(
        reduce({'+': add, '*': mul}[op], group)
        for group, op in zip(numbers, operators)
    )
)

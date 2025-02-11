from typing import Iterator
import operator as op
from itertools import product
from functools import reduce

Rule = tuple[int, list[int]]
Rules = list[Rule]


def load(filename: str) -> Rules:
    def get_rule(s: str) -> Rule:
        result, components_str = s.split(': ')
        return int(result), list(map(int, components_str.split()))

    with open(filename) as f:
        return [get_rule(row) for row in f]


rules = load('input.txt')


def eval(components: list[int], ops: list) -> Iterator[int]:
    possibilities = product(
        ops, repeat=len(components) - 1
    )

    def compute(ops: list):
        return reduce(
            lambda x, y: y[0](x, y[1]), zip(ops, components[1:]),
            components[0]
        )

    yield from map(compute, possibilities)


print(
    sum(
        res
        for res, components in rules
        if res in set(eval(components, [op.__mul__, op.__add__]))
    )
)


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


print(
    sum(
        res
        for res, components in rules
        if res in set(eval(components, [op.__mul__, op.__add__, concat]))
    )
)

from typing import Iterable, Generator
from itertools import islice
import re
import numpy as np


def batched(it: Iterable, n: int) -> Generator:
    it = iter(it)
    while batch := tuple(islice(it, n)):
        if len(batch) < n:
            raise ValueError(f'Batch is of size {len(batch)} < {n}.')
        yield batch


def parse(filename: str) -> list[tuple]:
    configs = []
    with open(filename) as f:
        for config_str in f.read().split('\n\n'):
            a, b, prize = batched(map(int, re.findall(r'\d+', config_str)), 2)
            configs.append((a, b, prize))
    return configs


def solve(config: tuple) -> int:
    a, b, prize = config

    if (a[0] / b[0]) == (a[1] / b[1]):
        raise ValueError('Colinear')
    solution = np.linalg.solve(np.array([a, b]).T, np.array(prize))
    if (
        (solution[0] < 0) or
        (solution[1] < 0) or
        (abs(solution[0] - round(solution[0])) > 1e-6) or
        (abs(solution[1] - round(solution[1])) > 1e-6)
    ):
        return 0
    print(solution)
    return (
        solution @
        np.array([3, 1])
    )


def solve_bruteforce(config: tuple) -> int:
    a, b, prize = config

    a_1, a_2 = a
    b_1, b_2 = b
    p_1, p_2 = prize
    for x in range(1, 101):
        for y in range(1, 101):
            cond_x = (x * a_1 + y * b_1) == p_1
            cond_y = (x * a_2 + y * b_2) == p_2
            if cond_x and cond_y:
                return 3*x + y
    return 0


configs = parse('input.txt')

sol1 = [solve_bruteforce(c) for c in configs]


sol2 = list(
    map(
        lambda x: int(round(x)),
        (solve(c) for c in configs)
    )
)

print(sum(sol1), sum(sol2))


def mod_config(c: tuple) -> tuple:
    a, b, prize = c
    shift = 10000000000000
    return (a, b, (prize[0] + shift, prize[1] + shift))


print(
    sum(
        map(
            lambda x: int(round(x)),
            (solve(mod_config(c)) for c in configs)
        )
    )
)

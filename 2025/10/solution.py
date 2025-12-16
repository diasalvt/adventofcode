from itertools import product, compress
from functools import reduce
import operator
import numpy as np


Puzzle = tuple[
    tuple[bool, ...], list[int],
    set[int]
]


def load(filename: str) -> list[Puzzle]:
    with open(filename) as f:
        lines = f.read().splitlines()

    result = []
    for line in lines:
        press, *buttons, joltage = line.split()
        press = tuple(
            True if c == '#' else False for c in press[1:-1]
        )
        button_positions = [
            tuple(int(b_i) for b_i in button[1:-1].split(','))
            for button in buttons
        ]
        buttons = [
            tuple(i in button_position for i in range(len(press)))
            for button_position in button_positions
        ]

        joltage = [
            int(j_i)
            for j_i in joltage[1:-1].split(',')
        ]
        result.append((press, buttons, joltage))

    return result


def xor(*t: tuple[bool, ...]) -> tuple[bool, ...]:
    return tuple(reduce(operator.xor, t_i) for t_i in zip(*t))


puzzles = load('test.txt')


result = sum(
    min(
        sum(selection)
        for selection in product((0, 1), repeat=len(buttons))
        if xor(*compress(buttons, selection)) == press
    )
    for press, buttons, _ in puzzles
)

print(result)

matrix_res = [
    (np.array(buttons).astype(int).T, np.array([count]).T)
    for _, buttons, count in puzzles
]

results = [
    sum(np.round(np.linalg.lstsq(matrix, res)[0]))
    for matrix, res in matrix_res
]

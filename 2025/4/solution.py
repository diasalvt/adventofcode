from itertools import product
from typing import Iterable

Pos = complex
Grid = dict[Pos, str]


def load(filename: str) -> Grid:
    grid = {}
    with open(filename) as f:
        for y, row in enumerate(f.read().splitlines()):
            for x, c in enumerate(row):
                grid[x + y * 1j] = c
    return grid


def neighbours(p: Pos, g: Grid) -> Iterable[str]:
    for shift_x in (-1, 0, 1):
        for shift_y in (-1j, 0, 1j):
            shifted_p = p + shift_x + shift_y
            if (shifted_p != p) and (shifted_p in g):
                yield g[shifted_p]


g = load('input.txt')


def update(g: Grid) -> tuple[int, Grid]:
    to_remove = [
        p
        for p in g
        if (
            (g[p] == '@') and
            (sum(1 for n in neighbours(p, g) if n == '@') < 4)
        )
    ]
    return (
        len(to_remove),
        {
            p: g[p] if p not in to_remove else '.'
            for p in g
        }
    )


print(update(g)[0])
count = None
total = 0
while count != 0:
    count, g = update(g)
    total += count
print(total)

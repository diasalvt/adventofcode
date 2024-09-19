from typing import Generator
from itertools import pairwise


def parse(filename) -> list[tuple[complex, int]]:
    pointer = {'R': -1j, 'L': 1j}

    with open(filename) as f:
        moves = f.readline().strip().split(', ')
        moves = [(pointer[dir], int(''.join(steps))) for dir, *steps in moves]
    return moves


moves = parse('input.txt')


def walk(path: list[tuple[complex, int]]) -> Generator:
    current_dir = 1j
    current_pos = complex(0, 0)
    for dir, steps in moves:
        current_dir *= dir
        current_pos += current_dir * steps
        yield current_pos


*_, last = walk(moves)
print(abs(last.real) + abs(last.imag))


def full_walk(path: list[tuple[complex, int]]) -> Generator:
    current_dir = 1j
    current_pos = complex(0, 0)
    for dir, steps in moves:
        current_dir *= dir
        for _ in range(steps):
            current_pos += current_dir
            yield current_pos


seen_pos = set()
for pos in full_walk(moves):
    if pos in seen_pos:
        break
    seen_pos.add(pos)

print(abs(pos.real) + abs(pos.imag))

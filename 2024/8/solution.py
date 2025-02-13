from collections import defaultdict
from itertools import permutations
import operator as op
from functools import reduce


Pos = complex
Plan = tuple[dict[str, list[Pos]], tuple[int]]


def load(filename: str) -> Plan:
    with open(filename) as f:
        plan = defaultdict(list)
        for j, row in enumerate(f.read().splitlines()):
            for i, c in enumerate(row):
                if c != '.':
                    plan[c].append(i + j * 1j)
    return plan, (i + 1, j + 1)


plan = load('input.txt')


def antinodes_positions(
    positions: list[Pos], sizes: tuple[int], max_steps: int = 1
) -> int:
    antinodes = set()
    for p1, p2 in permutations(positions, 2):
        for i in range(1, max_steps + 1):
            n_p1 = p2 + i * (p2 - p1)
            if (
                (0 <= n_p1.real <= sizes[0] - 1) and
                (0 <= n_p1.imag <= sizes[1] - 1)
            ):
                antinodes |= {n_p1}

    return antinodes


print(
    len(
        reduce(
            op.__or__,
            (
                antinodes_positions(positions, plan[1])
                for antenna, positions in plan[0].items()
            )
        )
    )
)


print(
    (
        len(
            set().union(*plan[0].values()) |
            reduce(
                op.__or__,
                (
                    antinodes_positions(positions, plan[1], plan[1][0])
                    for antenna, positions in plan[0].items()
                )
            )
        )
    )
)

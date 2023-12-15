from itertools import combinations
from collections import defaultdict
from functools import reduce

Pos = tuple[int, int]


def load(filename: str) -> list[Pos]:
    return [
        (x, y)
        for y, line in enumerate(open(filename))
        for x, letter in enumerate(line.strip())
        if letter == '#'
    ]


galaxies = load('input.txt')
galaxies_test_not_expanded = load('test_not_expanded.txt')
galaxies_test = load('test_expanded.txt')


def add(p1: Pos, p2: Pos) -> Pos:
    return tuple(sum(p1_p2_i) for p1_p2_i in zip(p1, p2))


def add_dim(p: Pos, val: int, dim: int) -> Pos:
    return tuple(p_i + (val if i == dim else 0) for i, p_i in enumerate(p))


def expand(galaxies: list[Pos], multiplier: int = 2) -> list[Pos]:

    def expand_dim(galaxies: list[Pos], dim: int) -> list[Pos]:
        max_dim = max(pos[dim] for pos in galaxies)
        empty_spaces = (
            set(range(max_dim + 1)) -
            set(pos[dim] for pos in galaxies)
        )

        adder = reduce(
            lambda x, y: [
                v + (multiplier - 1 if i > y else 0) for i, v in enumerate(x)
            ],
            empty_spaces,
            [0] * (max_dim + 1)
        )

        return [
            add_dim(pos, adder[pos[dim]], dim)
            for pos in galaxies
        ]

    for dim in [0, 1]:
        galaxies = expand_dim(galaxies, dim)

    return galaxies


def manhattan(p1: Pos, p2: Pos) -> int:
    return sum(abs(p1_i - p2_i) for p1_i, p2_i in zip(p1, p2))


def display(galaxies: list[Pos]):
    max_x, max_y = map(max, zip(*galaxies))

    for y in range(max_y + 1):
        print(''.join(
            ['#' if (x, y) in galaxies else '.' for x in range(max_x + 1)]
        ))


print(
    sum(manhattan(p1, p2) for p1, p2 in combinations(expand(galaxies), 2))
)

print(
    sum(manhattan(p1, p2) for p1, p2 in combinations(expand(galaxies, 1e6), 2))
)

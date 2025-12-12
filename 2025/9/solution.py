from itertools import pairwise, chain, starmap, tee, islice, takewhile, count
from typing import Iterable
import matplotlib.pyplot as plt

Pos = tuple[int, ...]


def load(filename: str) -> list[Pos]:
    with open(filename) as f:
        return [tuple(map(int, r.split(','))) for r in f]


positions = load('input.txt')

result = max(
    (abs(p1_x - p2_x) + 1) * (abs(p1_y - p2_y) + 1)
    for p1_x, p1_y in positions
    for p2_x, p2_y in positions
    if (p1_x, p1_y) < (p2_x, p2_y)
)

print(result)


def gen_line(p1: Pos, p2: Pos) -> list[Pos]:
    if p1[0] == p2[0]:
        if p2[1] < p1[1]:
            return [(p1[0], y) for y in reversed(range(p2[1] + 1, p1[1] + 1))]
        else:
            return [(p1[0], y) for y in range(p1[1], p2[1])]
    else:
        if p2[0] < p1[0]:
            return [(x, p1[1]) for x in reversed(range(p2[0] + 1, p1[0] + 1))]
        else:
            return [(x, p1[1]) for x in range(p1[0], p2[0])]


def rectangle(p1: Pos, p2: Pos) -> list[Pos]:
    p1_x, p1_y = p1
    p2_x, p2_y = p2
    corner_1 = p1_x, p2_y
    corner_2 = p2_x, p1_y

    return set(
        gen_line(p1, corner_1) + gen_line(corner_1, p2) +
        gen_line(p2, corner_2) + gen_line(corner_2, p1)
    )


Segments = list[tuple[Pos, Pos]]
segments = list(pairwise(positions + [positions[0]]))


def nwise(it: Iterable, n: int = 3) -> Iterable:
    return zip(*(islice(it, i, None) for i, it in enumerate(tee(it, n))))


def build_border(segments: Segments, exterior: complex = -1) -> list[Pos]:
    border = list(
        starmap(
            complex,
            chain.from_iterable(
                gen_line(*s)
                for s in segments
            )
        )
    )

    external_border = [border[0] + exterior]
    for p1, p2, p3 in nwise(border + [border[0]]):
        dir_1, dir_2 = (p2 - p1), (p3 - p2)
        turn = dir_2 / dir_1
        if turn == 1:
            external_border += [external_border[-1] + dir_1]
        elif turn == -exterior:
            external_border += [
                external_border[-1] + dir_1,
                external_border[-1] + 2 * dir_1,
                external_border[-1] + 2 * dir_1 + dir_2,
            ]

    return border, set(external_border)


def rectangle_is_interior(
    p1: Pos, p2: Pos, external_border: set[Pos]
):
    return not any(
        complex(*p) in external_border
        for p in rectangle(p1, p2)
    )


def point_range(
    p: Pos, border: list[Pos], external_border: set[Pos]
) -> tuple:
    max_up, max_down, max_left, max_right = (
        list(takewhile(
            lambda p: p not in external_border,
            (complex(*p) + i * d for i in count())
        ))
        for d in [1j, -1j, -1, 1]
    )
    return (
        min(e.imag for e in max_left),
        max(e.real for e in max_right),
        min(e.imag for e in max_down),
        max(e.imag for e in max_up),
    )


for p1, p2 in segments:
    x_coord, y_coord = zip(p1, p2)
    plt.plot(x_coord, y_coord)

plt.show()

border, external_border = build_border(segments, -1)

result = 0
for p1 in positions:
    min_x, max_x, min_y, max_y = point_range(p1, border, external_border)
    for p2 in positions:
        if (min_x <= p2[0] <= max_x) and (min_y <= p2[1] <= max_y):
            area = (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
            if (p1 < p2) and (area > result):
                if rectangle_is_interior(p1, p2, external_border):
                    result = max(result, area)

print(result)

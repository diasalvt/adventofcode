from itertools import pairwise, chain, starmap, tee, islice
from typing import Iterable
from collections import defaultdict
from bisect import bisect_left, bisect_right
import tqdm

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


def rectangle_segments(p1: Pos, p2: Pos) -> tuple:
    min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
    min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])

    return (
        (min_x, max_x, range(min_y, max_y + 1)),
        (min_y, max_y, range(min_x, max_x + 1))
    )

Segments = list[tuple[Pos, Pos]]
segments = list(pairwise(positions + [positions[0]]))


def nwise(it: Iterable, n: int = 3) -> Iterable:
    return zip(*(islice(it, i, None) for i, it in enumerate(tee(it, n))))


def build_border(segments: Segments, exterior: complex = -1) -> tuple:
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
    skip = False

    for p1, p2, p3 in nwise(border + border[:2]):
        if not skip:
            exterior = external_border[-1] - p1
            dir_1, dir_2 = (p2 - p1), (p3 - p2)
            turn = dir_2 / dir_1
            if turn == 1:
                external_border += [external_border[-1] + dir_1]
            elif dir_2 == -exterior:
                external_border += [
                    external_border[-1] + dir_1,
                    external_border[-1] + 2 * dir_1,
                    external_border[-1] + 2 * dir_1 + dir_2,
                ]
            else:
                skip = True
        else:
            skip = False

    return border, external_border


Scanner = tuple[dict, ...]


def build_scanner(external_border: list[complex]) -> Scanner:
    x_y = defaultdict(set)
    y_x = defaultdict(set)
    for p in external_border:
        p_x, p_y = p.real, p.imag
        x_y[p_x] |= {p_y}
        y_x[p_y] |= {p_x}

    def to_sorted(d: defaultdict) -> defaultdict:
        return defaultdict(list, {
            k: sorted(v)
            for k, v in d.items()
        })
    return (to_sorted(x_y), to_sorted(y_x))


def rectangle_is_interior(
    p1: Pos, p2: Pos, scanner: Scanner
):
    x_y, y_x = scanner
    (x1, x2, r_y), (y1, y2, r_x) = rectangle_segments(p1, p2)
    return not(
        values_in_range(x_y[x1], r_y) or
        values_in_range(x_y[x2], r_y) or
        values_in_range(y_x[y1], r_x) or
        values_in_range(y_x[y2], r_x)
    )


def values_in_range(values: list, r: range) -> bool:
    start, end = r.start, r.stop - 1
    return len(
        values[bisect_left(values, start):bisect_right(values, end)]
    ) > 0


border, external_border = build_border(segments, 1)
scanner = build_scanner(external_border)

result = (0, (0, 0), (0, 0))
for p1 in tqdm.tqdm(positions):
    for p2 in positions:
        area = (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
        if (p1 < p2) and (area > result[0]):
            if rectangle_is_interior(p1, p2, scanner):
                result = max(result, (area, p1, p2))

print(result)

import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots()
for p1, p2 in segments:
    x_coord, y_coord = zip(p1, p2)
    ax.plot(x_coord, y_coord)

ax.plot(
    [v.real for v in external_border],
    [v.imag for v in external_border],
    color='black'
)

rect = patches.Rectangle(
    result[1], result[2][0] - result[1][0],
    result[2][1] - result[1][1],
    linewidth=1, edgecolor='r', facecolor='none'
)

ax.add_patch(rect)
plt.show()

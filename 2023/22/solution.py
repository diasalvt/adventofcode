from dataclasses import dataclass, field
from typing import TypeAlias, Self
from itertools import product
import re
from queue import PriorityQueue

Pos: TypeAlias = list[int]


@dataclass
class Brick:
    start: Pos
    end: Pos
    idx: int
    bricks_below: set[int] = field(default_factory=set)
    bricks_above: set[int] = field(default_factory=set)

    @classmethod
    def from_str(cls, s: str, i: int) -> Self:
        x1, y1, z1, x2, y2, z2 = map(int, re.findall(r'\d+', s))
        start = list(min((x1, y1, z1), (x2, y2, z2)))
        end = list(max((x1, y1, z1), (x2, y2, z2)))
        return cls(start, end, i)


def load(filename: str) -> list[Brick]:
    with open(filename) as f:
        bricks = sorted(
            [Brick.from_str(line, 0) for line in f],
            key=lambda x: x.start[2]
        )
    for i, _ in enumerate(bricks):
        bricks[i].idx = i
    return bricks


bricks = load('input.txt')
test = load('test.txt')


Bottom = dict[Pos, Brick]


def grow_bottom(bottom: Bottom, brick: Brick) -> Bottom:
    start, end = brick.start, brick.end
    x_range, y_range = range(start[0], end[0] + 1), range(start[1], end[1] + 1)

    highest_z = max(
        (
            bottom[(x, y)].end[2]
            for x, y in product(x_range, y_range)
            if (x, y) in bottom
        ), default=0
    )

    z_move = highest_z + 1 - brick.start[2]
    brick.start[2] += z_move
    brick.end[2] += z_move

    for x, y in product(x_range, y_range):
        if (x, y) in bottom and (bottom[(x, y)].end[2] == highest_z):
            brick.bricks_below.add(bottom[(x, y)].idx)
            bottom[(x, y)].bricks_above.add(brick.idx)
        bottom[(x, y)] = brick

    return bottom


def process(bricks: list[Brick]) -> tuple[list[Brick], Bottom]:
    bottom = {}
    for brick in bricks:
        bottom = grow_bottom(bottom, brick)

    return bricks


def count_can_be_disintegrated(bricks: list[Brick]) -> int:
    r = 0
    for brick in bricks:
        r += all(
            bricks[b_idx].bricks_below - {brick.idx}
            for b_idx in brick.bricks_above
        )
    return r


process(bricks)
print(count_can_be_disintegrated(bricks))


def collapse(bricks: list[Brick], idx: int) -> int:
    collapsed = set()
    pqueue = PriorityQueue()
    pqueue.put((bricks[idx].start[2], idx))

    while not pqueue.empty():
        _, to_collapse = pqueue.get()
        collapsed.add(to_collapse)
        bricks_above_to_collapse = {
            b_idx
            for b_idx in bricks[to_collapse].bricks_above
            if bricks[b_idx].bricks_below.issubset(collapsed)
        }
        for b_idx in bricks_above_to_collapse:
            pqueue.put((bricks[b_idx].start[2], b_idx))

    return len(collapsed) - 1


def total_collapse(bricks: list[Brick]) -> int:
    return sum(collapse(bricks, idx) for idx, _ in enumerate(bricks))


print(total_collapse(bricks))

from dataclasses import dataclass
from itertools import pairwise, islice, tee
from typing import Self, Generator, Optional, Iterable
from enum import Enum


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def __add__(self, other) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y)

    @classmethod
    def from_str(cls, s: str) -> Self:
        x, y = s.split(',')
        return cls(int(x), int(y))

    def next(self, elem_map: 'Map') -> Self:
        for p in [Pos(0, 1), Pos(-1, 1), Pos(1, 1)]:
            if (n := p + self) not in elem_map:
                return n
        return self

    def __iter__(self):
        return iter([self.x, self.y])

    def __rshift__(self, other: Self) -> Generator:
        """
            Get a line between 2 Positions
        """
        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                yield self.__class__(x1, y)
        else:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                yield self.__class__(x, y1)


def parse_file(filename: str) -> list[list[Pos]]:
    with open(filename) as f:
        return [
            [Pos.from_str(s) for s in row.split(' -> ')]
            for row in f.read().splitlines()
        ]


print(parse_file('test.txt'))


class Elem(Enum):
    ROCK = 1
    SAND = 2
    START = 3


class Map:

    def __init__(self, rocks: list[list[Pos]]) -> Self:
        self.start = Pos(500, 0)
        rock_map: dict[Pos, Elem] = {self.start: Elem.START}

        for line_rock in rocks:
            for p1, p2 in pairwise(line_rock):
                for p_x, p_y in p1 >> p2:
                    rock_map[Pos(p_x, p_y)] = Elem.ROCK
        self.rock_map = rock_map

    def __contains__(self, obj) -> bool:
        return obj in self.rock_map

    def __repr__(self) -> str:
        s = ''
        y = [k.y for k in self.rock_map]
        x = [k.x for k in self.rock_map]
        height = max(y) - min(y) + 1
        width = max(x) - min(x) + 1

        def pos_to_char(p: Pos) -> str:
            char = {
                Elem.ROCK: '#',
                Elem.SAND: 'o',
                Elem.START: '+'
            }

            if p == Pos(500, 0):
                return '+'
            else:
                return char[self.rock_map[p]] if p in self.rock_map else '.'

        for i in range(height):
            s += ''.join([pos_to_char(Pos(j + min(x), i + min(y)))
                         for j in range(width)])
            s += '\n'

        return s

    # None if sand fall infinitely
    def liberate_sand(self, floor=False) -> Optional[Pos]:
        curr_pos = self.start
        while (next_pos := curr_pos.next(self)) != curr_pos:
            curr_pos = next_pos
            if curr_pos.y >= max([k.y for k in self.rock_map]):
                return None
        return curr_pos

    def __iter__(self):
        return self

    def __next__(self):
        p = self.liberate_sand()
        if p is None:
            raise StopIteration
        else:
            self.rock_map[p] = Elem.SAND
            return self


def test_map():
    elem_map = Map(parse_file('test.txt'))
    len([m for m in elem_map]) == 24


def part_1(filename: str) -> int:
    return len([m for m in Map(parse_file(filename))])


print(part_1('test.txt'))
print(part_1('input.txt'))


def nwise(it: Iterable, n: int) -> Generator:
    return zip(*(islice(g, i, None) for i, g in enumerate(tee(it, n))))


def can_be_seen(
    prev: list[bool], starting_pos: Pos, elem_map: Map
) -> list[bool]:

    def available(pos: Pos, prev_availability: list[bool]):
        a, b, c = prev_availability
        if a or b or c:
            return pos not in elem_map
        else:
            return False

    return (
        [False]*2 +
        [
            available(starting_pos + Pos(i, 0), w_prev)
            for i, w_prev in enumerate(nwise(prev, 3))
        ] +
        [False]*2
    )


def part_2(filename: str):
    elem_map = Map(parse_file(filename))
    height = max([p.y for p in elem_map.rock_map]) + 2
    can_see = [
        False,
        True,
        False,
    ]

    res = 0
    for i in range(height):
        can_see = can_be_seen(can_see, Pos(500 - i - 1, i), elem_map)
        res += sum(can_see)
    return res


print(part_2('input.txt'))

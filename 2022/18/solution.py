from typing import NamedTuple, Self, Union
from operator import add
from itertools import starmap, product
import re


class Pos(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: Union[Self, tuple[int, int, int]]) -> Self:
        return self.__class__(*starmap(add, zip(self, other)))


# print(Pos(1, 2, 0) + Pos(1, 0, 0))
# print(Pos(1, 2, 0) + (1, 0, 0))


def parse_file(filename: str) -> set[Pos]:
    with open(filename) as f:
        return {
            Pos(*map(int, re.findall(r'-?\d+', row)))
            for row in f.read().splitlines()
        }


test = parse_file('test.txt')
# print(test)


def neighborhood(pos: Pos) -> set[Pos]:
    neighbours_pos = set()
    for axis in range(3):
        for dir in [-1, 1]:
            shift = [0]*3
            shift[axis] = dir
            neighbours_pos.add(pos + tuple(shift))
    return neighbours_pos


def count_exposed_faces(cubes: set[Pos]) -> int:
    count_hidden = 0
    for cube in cubes:
        count_hidden += sum(
            neighbour in cubes for neighbour in neighborhood(cube)
        )
    return 6 * len(cubes) - count_hidden


# print(count_exposed_faces(parse_file('minitest.txt')))
# print(count_exposed_faces(test))

print(count_exposed_faces(parse_file('input.txt')))


def air_cubes(cubes: set[Pos]) -> int:
    min_x, max_x = min(c.x for c in cubes) - 1, max(c.x for c in cubes) + 1
    min_y, max_y = min(c.y for c in cubes) - 1, max(c.y for c in cubes) + 1
    min_z, max_z = min(c.z for c in cubes) - 1, max(c.z for c in cubes) + 1
    range_x = range(min_x, max_x + 1)
    range_y = range(min_y, max_y + 1)
    range_z = range(min_z, max_z + 1)
    ranges = (range_x, range_y, range_z)

    total_size = len(range_x) * len(range_y) * len(range_z)

    air = (
        {Pos(x, y, min_z) for x, y in product(range_x, range_y)} |
        {Pos(x, y, max_z) for x, y in product(range_x, range_y)} |
        {Pos(x, min_y, z) for x, z in product(range_x, range_z)} |
        {Pos(x, max_y, z) for x, z in product(range_x, range_z)} |
        {Pos(min_x, y, z) for z, y in product(range_z, range_y)} |
        {Pos(max_x, y, z) for z, y in product(range_z, range_y)}
    )

    air_front = air

    def is_inside(pos: Pos, ranges: list) -> bool:
        return all(
            c in r_c for c, r_c in zip(pos, ranges)
        )

    while air_front:
        next_air_front = set()
        for air_cube in air_front:
            for n in neighborhood(air_cube):
                if (n not in air) and (n not in cubes) and is_inside(n, ranges):
                    next_air_front.add(n)
        air_front = next_air_front
        air |= air_front

    return {
        pos
        for pos in starmap(Pos, product(*ranges))
        if (pos not in air) and (pos not in cubes)
    }


# print(air_cubes({Pos(0, 0, 0), Pos(1, 1, 0), Pos(2, 0, 0), Pos(1, -1, 0), Pos(1, 0, 1), Pos(1, 0, -1)}))
cubes = parse_file('input.txt')
print(count_exposed_faces(cubes | air_cubes(cubes)))

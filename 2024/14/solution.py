import re
from itertools import product
from functools import reduce
from collections import Counter

Pos = Vel = complex
Robot = tuple[Pos, Vel]
Terrain = tuple[int, int]


def load(filename: str) -> list[Robot]:
    def create_robot(p_x: int, p_y: int, v_x: int, v_y: int) -> Robot:
        return (p_x + 1j * p_y, v_x + 1j * v_y)

    with open(filename) as f:
        return [
            create_robot(*map(int, re.findall(r'-?\d+', row)))
            for row in f
        ]


robots = load('input.txt')
terrain: Terrain = (101, 103)
quadrants: tuple[tuple[range]] = tuple(product(
    (
        range(terrain[0] // 2),
        range(terrain[0] // 2 + 1, terrain[0])
    ),
    (
        range(terrain[1] // 2),
        range(terrain[1] // 2 + 1, terrain[1])
    )
))


def update_pos(pos: Pos, v: Vel, terrain: Terrain = terrain) -> Pos:
    t_x, t_y = terrain

    new_pos = pos + v
    return (new_pos.real % t_x) + 1j * (new_pos.imag % t_y)


def is_in(pos: Pos, quadrant: tuple[range, range]) -> bool:
    p_x, p_y = pos.real, pos.imag
    return (p_x in quadrant[0]) and (p_y in quadrant[1])


def display(robots: list[Pos], terrain: Terrain) -> None:
    robots_set = set(robots)
    for y in range(terrain[1]):
        row = ''.join(
            '*' if (x + 1j * y) in robots_set else '_'
            for x in range(terrain[0])
        )
        print(row)


result = reduce(
    lambda x, y: x * y,
    [
        sum(is_in(update_pos(p, 100 * v), q) for p, v in robots)
        for q in quadrants
    ]
)

print(result)

for i in range(100_000, 500_000):
    result_quadrants = [
        sum(is_in(update_pos(p, i * v), q) for p, v in robots)
        for q in quadrants
    ]
    if (
        (result_quadrants[0] == result_quadrants[1]) and
        (result_quadrants[2] == result_quadrants[3])
    ):
        print(i)
        display([update_pos(p, i * v, terrain) for p, v in robots], terrain)
        print('\n\n')

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
terrain = (
    1 + max(int(p.real) for p, v in robots),
    1 + max(int(p.imag) for p, v in robots)
)

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


def update_robots(
    robots: list[Robot], steps: int, terrain: Terrain
) -> list[Pos]:
    return [update_pos(p, steps * v, terrain) for p, v in robots]


def is_in(pos: Pos, quadrant: tuple[range, range]) -> bool:
    p_x, p_y = pos.real, pos.imag
    return (p_x in quadrant[0]) and (p_y in quadrant[1])


def display(positions: list[Pos], terrain: Terrain) -> None:
    positions_set = set(positions)
    for y in range(terrain[1]):
        row = ''.join(
            '*' if (x + 1j * y) in positions_set else '_'
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


"""
    First idea was to look at the 'entropy' of the image.
    If the image is random, we expect the robots to no be concentrated
    anywhere.
    But this filter was not specific enough.
    Looking at the final picture, it could work if we look at the last
    quartile.
"""
# def entropy(positions: list[Pos], terrain: Terrain, zoom: int = 20) -> float:
#     t_x, t_y = terrain

#     c = Counter(p.real // zoom + 1j * (p.imag // zoom) for p in positions)
#     return sum(c.values()) / len(c.values())


def count_symmetric(positions: list[Pos], terrain: Terrain) -> bool:
    t_x, _ = terrain
    middle = t_x // 2

    counter_positions = Counter(positions)
    return sum(
        (
            counter_positions[p] ==
            counter_positions[
                p +
                2 * (p.real - middle if p.real < middle else middle - p.real)
            ]
        )
        for p in positions
    )


def scan(robots: list[Robot], terrain: Terrain) -> int:
    res = []
    t_x, t_y = terrain
    for i in range(t_x * t_y):
        updated_pos = update_robots(robots, i, terrain)
        res.append(count_symmetric(updated_pos, terrain))

    return res


result = max(enumerate(scan(robots, terrain)), key=lambda x: x[1])
print(result)

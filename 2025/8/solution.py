from math import sqrt
from functools import reduce
from itertools import islice
from operator import mul
import matplotlib.pyplot as plt

Pos = tuple[int]


def load(filename: str) -> list[Pos]:
    with open(filename) as f:
        return [
            tuple(int(s) for s in row.split(','))
            for row in f
        ]


positions = load('input.txt')


def euclidean_distance(p1: Pos, p2: Pos) -> float:
    return sqrt(sum((p_1_i - p_2_i)**2 for p_1_i, p_2_i in zip(p1, p2)))


def all_distances(positions: list[Pos]) -> list[tuple[tuple[Pos, Pos], float]]:
    distances = [
        (euclidean_distance(p1, p2), p1, p2)
        for p1 in positions
        for p2 in positions
        if p1 < p2
    ]

    return sorted(distances)


def build_groups(
    positions: list[Pos],
    limit: int = 1000
) -> set[frozenset] | tuple[Pos, Pos]:
    groups = {
        p: frozenset({p})
        for i, p in enumerate(positions)
    }

    for _, p1, p2 in all_distances(positions)[:limit]:
        new_group = groups[p1] | groups[p2]
        for p in new_group:
            groups[p] = new_group
        if new_group == frozenset(p for p in positions):
            return p1, p2

    return set(groups.values())


result = reduce(
    mul,
    islice(sorted(map(len, build_groups(positions)), reverse=True), 3)
)

print(result)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(*zip(*positions))
plt.show()

p1, p2 = build_groups(positions, limit=len(positions)**2)
print(p1[0] * p2[0])

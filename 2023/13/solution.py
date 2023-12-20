import numpy as np
from functools import reduce


Terrain = np.ndarray


def load(filename: str) -> list[Terrain]:
    with open(filename) as f:
        terrains_str = f.read().split('\n\n')
        return [
            np.array([list(row) for row in terrain.splitlines()])
            for terrain in terrains_str
        ]


terrains = load('input.txt')
terrains_test = load('test.txt')


def count_differences(arr1: np.ndarray, arr2: np.ndarray) -> bool:
    return sum(
        sum(r1 != r2) for r1, r2 in zip(np.flip(arr1, axis=0), arr2)
    )


def reflection_indexes_rows(terrain: Terrain, smudges: int = 0) -> list[int]:
    mirror_indexes = []
    for i in range(1, len(terrain)):
        top, bottom = terrain[:i, ...], terrain[i:, ...]
        if count_differences(top, bottom) == smudges:
            mirror_indexes.append(i)
    return mirror_indexes


def reflection_indexes(
    terrain: Terrain, smudges: int
) -> tuple[list[int], list[int]]:
    return (
        reflection_indexes_rows(terrain, smudges),
        reflection_indexes_rows(terrain.transpose(), smudges)
    )


def solve(
    terrains: list[Terrain], smudges: int = 0
) -> int:
    return reduce(
        lambda x, y: x + sum(y[0]) * 100 + sum(y[1]),
        [reflection_indexes(terrain, smudges) for terrain in terrains],
        0
    )


print(solve(terrains, 0))
print(solve(terrains, 1))




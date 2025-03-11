from typing import Callable


Pos = complex
Topo = dict[Pos, int]


def load(filename: str) -> Topo:
    topo = {}
    with open(filename) as f:
        for i, row in enumerate(f):
            for j, c in enumerate(row):
                if c in '0123456789':
                    topo[j + i * 1j] = int(c)
    return topo


topo = load('input.txt')


def next(pos: Pos, topo: Topo) -> set[Pos]:
    return {
        pos + shift
        for shift in {1j, -1j, 1, -1}
        if (pos + shift in topo) and topo[pos + shift] == (topo[pos] + 1)
    }


def trailhead_score(
    pos: Pos, topo: Topo, target: int = 9, structure_next: Callable = set
) -> int:
    current = {pos}
    for i in range(topo[pos], target):
        current = structure_next(
            p for curr_p in current for p in next(curr_p, topo)
        )
    return len(current)


def score(topo: Topo, structure_next: Callable = set):
    return sum(
        trailhead_score(pos, topo, 9, structure_next)
        for pos in topo
        if topo[pos] == 0
    )


print(score(topo))
print(score(topo, list))

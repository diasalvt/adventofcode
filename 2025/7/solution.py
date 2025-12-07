from itertools import accumulate
from operator import add


def load(filename: str) -> list[list[int]]:
    with open(filename) as f:
        lines = f.read().splitlines()
    return [
        [i for i, c in enumerate(l) if c == '^']
        for l in lines[2::2]
    ]


d = load('input.txt')

result = 1
beams = {d[0][0] - 1, d[0][0] + 1}
for splitters in d[1:]:
    result += sum(s in beams for s in splitters)
    beams = {
        s + shift
        for s in splitters
        for shift in (-1, 1)
        if s in beams
    } | {b for b in beams if b not in splitters}

print(result)

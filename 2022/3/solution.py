from typing import Iterable, Generator
from itertools import tee

with open('input.txt') as f:
    sacks = f.read().splitlines()

def score(sacks: list[str]) -> int:

    common = [(set(sack[:len(sack)//2]) & set(sack[len(sack)//2:])).pop() for sack in sacks]
    return  sum(
        [
            ord(c) - ord('a') + (1 if c.islower() else ord('a') - ord('A') + 27)
            for c in common
        ]
    )

def test_score():
    with open('test.txt') as f:
        sacks = f.read().splitlines()

    assert score(sacks) == 157

print(score(sacks))

def score2(sacks: list[str]) -> int:

    def nwindow(it: Iterable, n: int) -> Generator:
        iterator = it.__iter__()
        while True:
            res = []
            for _ in range(n):
                try:
                    res.append(next(iterator))
                except StopIteration:
                    return
            yield res

    groups = nwindow(sacks, n=3)
    
    res = 0
    for e1, e2, e3 in groups:
        c = (set(e1) & set(e2) & set(e3)).pop()
        priority = ord(c) - ord('a') + (1 if c.islower() else ord('a') - ord('A') + 27)
        res += priority

    return res

def test_score2():
    with open('test.txt') as f:
            sacks = f.read().splitlines()

    assert score2(sacks) == 70

print(score2(sacks))

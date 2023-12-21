from itertools import pairwise, count
from collections import Counter


Terrain = tuple[str]


def transpose(terrain: Terrain) -> Terrain:
    return tuple(
        map(''.join, zip(*terrain))
    )


def load(filename: str) -> Terrain:
    '''
        Column oriented terrain
    '''
    return transpose(open(filename).read().splitlines())


terrain = load('input.txt')
terrain_test = load('test.txt')

def count_roll_top(terrain: Terrain) -> int:
    score = 0
    for col in terrain:
        indexes_blocks = (
            [None] +
            [j for j in range(len(col)) if col[j] == '#'] +
            [None]
        )
        for a, b in pairwise(indexes_blocks):
            a, b = a + 1 if a is not None else 0, b
            for s in range(sum(1 for c in col[a:b] if c == 'O')):
                score += len(col) - a - s
    return score


print(count_roll_top(terrain))


def roll_top(terrain: Terrain) -> Terrain:
    next_terrain = []
    for i, col in enumerate(terrain):
        res = ''
        indexes_blocks = (
            [None] +
            [j for j in range(len(col)) if col[j] == '#'] +
            [None]
        )
        for a, b in pairwise(indexes_blocks):
            a, b = a + 1 if a is not None else 0, b
            res += ''.join(sorted(col[a:b], reverse=True))
            res += '#'
        next_terrain.append(res[:-1])
    return tuple(next_terrain)


def turn_counter_clockwise(terrain: Terrain) -> Terrain:
    return tuple(map(''.join, zip(*map(reversed, terrain))))


def score(terrain: Terrain) -> int:
    return sum(
        sum(len(col) - i for i, char in enumerate(col) if char == 'O')
        for col in terrain
    )


def play(terrain: Terrain, n: int) -> Terrain:
    for i in range(n - 1):
        terrain = roll_top(terrain)
        terrain = turn_counter_clockwise(terrain)
    terrain = roll_top(terrain)
    for _ in range((5 - n) % 4):
        terrain = turn_counter_clockwise(terrain)
    return terrain


def find_cycle(terrain: Terrain) -> tuple[int, int]:
    seen_states = {}
    for i in count(1):
        terrain = roll_top(terrain)
        terrain = turn_counter_clockwise(terrain)
        if terrain in seen_states:
            return (seen_states[terrain], i)
        else:
            seen_states[terrain] = i

start, end = find_cycle(terrain)
cycle_size = end - start

to_play = (4_000_000_000 - start) % cycle_size + start

print(score(play(terrain, to_play)))

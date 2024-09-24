from itertools import product
from functools import reduce

Pos = complex

_DIRS = {
    'L': -1,
    'R': +1,
    'U': -1j,
    'D': +1j
}


def build_plan(n: int, m: int) -> dict[Pos, int]:
    plan = {}
    grid = product(range(n), range(m))
    for count, (row, col) in enumerate(grid, start=1):
        plan[col + row*1j] = count

    return plan


def get_pos(plan: dict, moves: str, start: Pos = 0) -> Pos:
    moves = map(lambda d: _DIRS[d], moves)
    return reduce(
        lambda pos, move: pos + (move if (pos + move) in plan else 0),
        moves,
        start
    )


def get_commands(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().splitlines()


def play(plan: dict, commands: list[str], start = 0) -> str:
    pos = start
    result = ''
    for moves in commands:
        pos = get_pos(plan, moves, pos)
        result += str(plan[pos])

    return result


plan = build_plan(3, 3)


def test_play():
    assert play(plan, get_commands('test.txt')) == '1985'


print(play(plan, get_commands('input.txt')))

"""
Hardcoded for simplicity, generic case is not interesting to me.
But this does not match previous type hinting due to A, B, C, ...
"""
plan_part2 = {
    0: 1,
    (-1 + 1j): 2,
    1j: 3,
    1 + 1j: 4,
    -2 + 2j: 5,
    -1 + 2j: 6,
    2j: 7,
    1 + 2j: 8,
    2 + 2j: 9,
    -1 + 3j: 'A',
    3j: 'B',
    1 + 3j: 'C',
    4j: 'D'
}


def test_play2():
    assert play(plan_part2, get_commands('test.txt'), start=(-2+2j)) == '5DB3'


print(play(plan_part2, get_commands('input.txt'), start=(-2+2j)))

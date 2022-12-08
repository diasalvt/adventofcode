from itertools import accumulate, chain
from typing import Iterable, Generator, Callable

Grid = list[list[int]]
Pos = tuple[int, int]
AugmentedGrid = list[list[tuple[Pos, int]]]


def parse_file(filename: str) -> Grid:
    with open(filename) as f:
        grid = [list(map(int, row)) for row in f.read().split()]

    return grid


test = parse_file('test.txt')
print(*test, sep='\n')


def visible_idx_from_left(grid: Grid) -> set[Pos]:
    def filter_row(i, row):
        return [
            (i, j)
            for j, (pred_max, curr_val)
            in enumerate(zip(accumulate(row, max, initial=-1), row))
            if pred_max < curr_val
        ]

    return {res for i, row in enumerate(grid) for res in filter_row(i, row)}


def left_to_right(positions: set[Pos], grid: Grid) -> set[Pos]:
    n = len(grid[0])
    return {(i, n - j - 1) for i, j in positions}


def left_to_top(positions: set[Pos], grid: Grid) -> set[Pos]:
    return {(j, i) for i, j in positions}


def left_to_bottom(positions: set[Pos], grid: Grid) -> set[Pos]:
    n = len(grid)
    return {(n - j - 1, i) for i, j in positions}


def inv_grid(g):
    return [list(reversed(row)) for row in g]


def tr_grid(g):
    return list(zip(*g))


def all_visible_pos(g: Grid) -> set[Pos]:
    from_left = visible_idx_from_left(g)
    from_right = left_to_right(visible_idx_from_left(inv_grid(g)), g)
    from_top = left_to_top(visible_idx_from_left(tr_grid(g)), g)
    from_bottom = left_to_bottom(
        visible_idx_from_left(inv_grid(tr_grid(g))), g
    )
    return from_left | from_right | from_top | from_bottom


def test_all_visible_pos():
    test = parse_file('test.txt')
    assert len(all_visible_pos(test)) == 21


print(len(all_visible_pos(grid := parse_file('input.txt'))))


def takeuntil(fn: Callable, it: Iterable) -> Generator:
    for elem in it:
        if fn(elem):
            yield elem
        else:
            yield elem
            return


def visibility_score(pos: Pos, g: Grid) -> Grid:
    i, j = pos
    val = g[i][j]
    before, after = g[i][:j], g[i][j+1:]
    t_g = tr_grid(g)
    up, down = t_g[j][:i], t_g[j][i+1:]

    _f = lambda x: sum(1 for _ in takeuntil(lambda y: y < val, x))

    return (
        _f(reversed(before)) *
        _f(after) *
        _f(reversed(up)) *
        _f(down)
    )


def final_score(g: Grid) -> int:
    return max(chain.from_iterable(
        [
            [visibility_score((i, j), g) for j, _ in enumerate(g)]
            for i, row in enumerate(g)
        ]
    ))


def test_visibility_score():
    test = parse_file('test.txt')
    assert final_score(test) == 8


print(final_score(grid))

from typing import Literal
from functools import reduce
from operator import add

Pos = complex
Elem = Literal['.', '#', 'S']
Map = dict[Pos, Elem]
_VALID_ELEM = ['.', 'S']


def load(filename: str) -> Map:
    puzzle_map = {}
    with open(filename) as f:
        for y, row in enumerate(f.read().splitlines()):
            for x, char in enumerate(row):
                puzzle_map[complex(x, y)] = char
    return puzzle_map


test_puzzle_map = load('test.txt')
test_puzzle_map2 = load('test_simplified.txt')


def neighbours(
    puzzle_map: Map, pos: Pos
) -> list[Pos]:
    shift_cross = [-1, 1, 1j, -1j]
    pos_cross = [pos + shift for shift in shift_cross]

    return [
        p
        for p in pos_cross
        if (p in puzzle_map.keys()) and (puzzle_map[p] in _VALID_ELEM)
    ]


def start(puzzle_map: Map) -> Pos:
    return next(filter(lambda x: x[1] == 'S', puzzle_map.items()))[0]


def run(puzzle_map: Map, steps: int = 1) -> set[Pos]:
    current_pos: set[Pos] = {start(puzzle_map)}
    puzzle_map_distance: dict[Pos, int] = {}

    for i in range(steps):
        current_pos = {
            next_p
            for p in current_pos
            for next_p in neighbours(
                puzzle_map, p
            )
        }
        for p in current_pos:
            if p not in puzzle_map_distance:
                puzzle_map_distance[p] = i
    return current_pos


def map_dim(puzzle_map: Map) -> tuple[int]:
    width = int(max(p.real for p in puzzle_map.keys()) + 1)
    height = int(max(p.imag for p in puzzle_map.keys()) + 1)

    return (width, height)


def display(puzzle_map: Map, positions: set[Pos]) -> None:
    width, height = map_dim(puzzle_map)
    shift_real = int(min(p.real for p in puzzle_map.keys()))
    shift_imag = int(min(p.imag for p in puzzle_map.keys()))

    def char(i: int, j: int) -> str:
        if complex(i, j) not in positions:
            return puzzle_map.get(complex(i, j), '.')
        else:
            return 'O'

    for j in range(shift_imag, shift_imag + height):
        print(
            ''.join(
                char(i, j)
                for i in range(shift_real, shift_real + width)
            )
        )


puzzle_map = load('input.txt')
print(len(run(puzzle_map, 64)))


def pos_repeat(pos: Pos, dim: tuple[int]) -> Pos:
    width, height = dim
    return complex(pos.real % width, pos.imag % height)


def neighbours_with_exclusion(
    puzzle_map: Map, pos: Pos,
    excluded: set[Pos],
    dim: tuple[int]
) -> set[Pos]:
    shift_cross = [-1, 1, 1j, -1j]
    pos_cross = [pos + shift for shift in shift_cross]

    return {
        p
        for p in pos_cross
        if (
            (puzzle_map[pos_repeat(p, dim)] in _VALID_ELEM) and
            (p not in excluded)
        )
    }


def run2(puzzle_map: Map, steps: int = 1) -> set[Pos]:
    count_n_1, count_n = 0, 0
    border_n_1, border_n = set(), {start(puzzle_map)}

    dim = map_dim(puzzle_map)

    for i in range(steps + 1):
        count_n, count_n_1 = count_n_1 + len(border_n), count_n
        border_n, border_n_1 = {
            next_p
            for p in border_n
            for next_p in neighbours_with_exclusion(
                puzzle_map, p, border_n_1, dim
            )
        }, border_n
    return count_n, border_n


# print(run2(puzzle_map, 26501365))


def area(n: int) -> int:
    return reduce(
        add,
        map(lambda x: 4 * x, range(1, n + 1)),
        1
    )


def covered(n: int) -> int:
    c_n, c_n_1 = 4, 1
    for i in range(2, n + 1):
        c_n, c_n_1 = 4 * i + c_n_1, c_n

    return c_n_1


def grid(
    puzzle_map: Map, repeat: int
) -> tuple[Map, dict]:
    repeated_map = {}
    sub_grid: dict[tuple[int, int], set[Pos]] = {}
    width, height = map_dim(puzzle_map)

    def shift_map(puzzle_map: Map, shift: complex) -> Map:
        return {
            p + shift: elem if elem != 'S' else '.'
            for p, elem in puzzle_map.items()
        }

    for x in range(repeat):
        for y in range(repeat):
            shifted_map = shift_map(
                puzzle_map, x * width + y * height * 1j
            )
            sub_grid[(x, y)] = set(shifted_map)
            repeated_map |= shifted_map

    middle = width * (repeat // 2) + width // 2
    repeated_map[middle + middle * 1j] = 'S'

    return repeated_map, sub_grid


def solve_puzzle(puzzle_map: Map, total_steps) -> int:

    repeat = 5
    big_test, sub_grid = grid(puzzle_map, repeat)
    width, height = map_dim(puzzle_map)
    fill_puzzle_map = run(big_test, (repeat * width - 1) // 2)

    sub_grid_count = {
        (x, y): sum(1 for p in fill_puzzle_map if p in positions)
        for (x, y), positions in sub_grid.items()
    }

    corners = sum(
        sub_grid_count[(x, y)] for x, y in [(0, 2), (2, 0), (2, 4), (4, 2)]
    )

    def count_tiles_filled(puzzle_map: Map, steps: int) -> tuple[int, int]:
        width, height = map_dim(puzzle_map)
        return int(((2 * steps + 1) / width - 1) // 2) + 1

    total_full_size = count_tiles_filled(puzzle_map, total_steps)

    total_inner = (
        covered(total_full_size - 1) * sub_grid_count[(2, 1)] +
        covered(total_full_size - 2) * sub_grid_count[(2, 2)]
    )

    outer_diag_size = total_full_size - 1
    total_outer_diag = outer_diag_size * sum(
        sub_grid_count[(x, y)]
        for x, y in [(1, 0), (1, 4), (3, 0), (3, 4)]
    )

    total_inner_diag = (outer_diag_size - 1) * sum(
        sub_grid_count[(x, y)]
        for x, y in [(1, 1), (1, 3), (3, 1), (3, 3)]
    )

    return (
        corners + total_inner + total_outer_diag + total_inner_diag
    )


puzzle_steps = 26501365
print(solve_puzzle(puzzle_map, puzzle_steps))

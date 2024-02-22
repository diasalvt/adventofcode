from collections import Counter
from typing import Literal, Optional
from tqdm import tqdm

Pos = complex
Elem = Literal['.', '#', 'S']
Map = dict[Pos, Elem]
_VALID_ELEM = ['.', 'S']


def load(filename: str) -> Map:
    map = {}
    with open(filename) as f:
        for y, row in enumerate(f.read().splitlines()):
            for x, char in enumerate(row):
                map[complex(x, y)] = char
    return map


test_map = load('test.txt')
test_map2 = load('test2.txt')


def neighbours(
    map: Map, pos: Pos
) -> list[Pos]:
    shift_cross = [-1, 1, 1j, -1j]
    pos_cross = [pos + shift for shift in shift_cross]

    return [
        p
        for p in pos_cross
        if (p in map.keys()) and (map[p] in _VALID_ELEM)
    ]


def start(map: Map) -> Pos:
    return next(filter(lambda x: x[1] == 'S', map.items()))[0]


def run(map: Map, steps: int = 1) -> set[Pos]:
    current_pos: set[Pos] = {start(map)}
    map_distance: dict[Pos, int] = {}

    for i in range(steps):
        current_pos = {
            next_p
            for p in current_pos
            for next_p in neighbours(
                map, p
            )
        }
        for p in current_pos:
            if p not in map_distance:
                map_distance[p] = i
    return current_pos


def display(map: Map, positions: set[Pos]) -> None:
    width = int(max(p.real for p in map.keys()) + 1)
    height = int(max(p.imag for p in map.keys()) + 1)

    for j in range(height):
        print(
            ''.join(
                map[complex(i, j)] if complex(i, j) not in positions else 'O'
                for i in range(width)
            )
        )


map = load('input.txt')
print(len(run(map, 64)))

# display(test_map2, run(test_map2, 10))


def neighbours_with_exclusion(
    map: Map, pos: Pos,
    excluded: set[Pos],
    dim: Optional[tuple[int]]
) -> set[Pos]:
    shift_cross = [-1, 1, 1j, -1j]
    pos_cross = [pos + shift for shift in shift_cross]

    def pos_repeat(pos: Pos) -> Pos:
        width, height = dim
        return complex(pos.real % width, pos.imag % height)

    return {
        p
        for p in pos_cross
        if (
            (map[pos_repeat(p)] in _VALID_ELEM) and
            (p not in excluded)
        )
    }


def run2(map: Map, steps: int = 1) -> set[Pos]:
    count_n_1, count_n = 0, 0
    border_n_1, border_n = set(), {start(map)}

    width = max(p.real for p in map.keys()) + 1
    height = max(p.imag for p in map.keys()) + 1
    dim = (width, height)

    for i in range(steps + 1):
        count_n, count_n_1 = count_n_1 + len(border_n), count_n
        border_n, border_n_1 = {
            next_p
            for p in border_n
            for next_p in neighbours_with_exclusion(map, p, border_n_1, dim)
        }, border_n
    return count_n


# print(run2(map, 26501365))
print(run2(test_map, 500))

for i in range(10):
    print(run2(test_map, i))


def neighbours_repeat(
    map: Map, pos: Pos,
    dim: Optional[tuple[int]]
) -> set[Pos]:
    shift_cross = [-1, 1, 1j, -1j]
    pos_cross = [pos + shift for shift in shift_cross]

    def pos_repeat(pos: Pos) -> Pos:
        width, height = dim
        return complex(pos.real % width, pos.imag % height)

    return {
        pos_repeat(p)
        for p in pos_cross
        if map[pos_repeat(p)] in _VALID_ELEM
    }


def run3(map: Map, steps: int = 1) -> Counter:
    p_n = Counter([start(map)])

    width = max(p.real for p in map.keys()) + 1
    height = max(p.imag for p in map.keys()) + 1
    dim = (width, height)

    c_n = []
    for _ in range(steps - 1):
        p_n = sum(
            (
                Counter({
                    next_pos: count
                    for next_pos in neighbours_repeat(map, pos, dim)
                })
                for pos, count in p_n.items()
            ),
            Counter()
        )
        c_n.append(sum(p_n.values()))

    return c_n[-1] - c_n[-2]

print(run3(test_map, 10))

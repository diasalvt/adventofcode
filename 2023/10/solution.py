from typing import Generator
from math import ceil

#
#      N
#     -j
# W -1   1 E
#      j
#      S
ConnectionType = set[complex]

connection_types: dict[str, ConnectionType] = {
    '|': {-1j, 1j},
    '-': {-1, 1},
    'L': {-1j, 1},
    'J': {-1, -1j},
    '7': {-1, 1j},
    'F': {1j, 1},
    'S': {-1, 1, 1j, -1j}
}

Pos = complex
Map = dict[Pos, ConnectionType]


def load(filename: str) -> Map:
    return {
        x + y * 1j: connection_types[letter]
        for y, line in enumerate(open(filename))
        for x, letter in enumerate(line.strip())
        if letter in connection_types
    }

map = load('input.txt')
map_test = load('test.txt')


def follow_pipe(pos: Pos, prev_pos: Pos, map: Map) -> Generator:
    while True:

        if pos not in map:
            return

        yield pos
        if map[pos] == connection_types['S']:
            return

        movement = next(iter(map[pos] - {prev_pos - pos}))
        prev_pos, pos = pos, pos + movement
        # Test compatibility
        if prev_pos - pos not in map[pos]:
            return


def solve_start(map: Map) -> list[Pos]:
    start = next(pos for pos, t in map.items() if t == connection_types['S'])

    for movement in [-1, +1, +1j, -1j]:
        path = list(follow_pipe(start + movement, start, map))
        if path and path[-1] == start:
            break

    return start, {path[0] - start, path[-2] - start}


def farthest(map: Map) -> int:
    start, start_type = solve_start(map)
    print(f'{start=}; {start_type}')
    dir1, dir2 = start_type

    return ceil(len(list(follow_pipe(start + dir1, -dir1, map))) / 2)


print(farthest(map))


def loop_map(map: Map) -> Map:
    start, start_type = solve_start(map)
    clean_path = list(follow_pipe(start + next(iter(start_type)), start, map))

    return {
        pos: t if pos != start else start_type
        for pos, t in map.items()
        if pos in clean_path
    }


loop = loop_map(map)


def is_interior(pos: Pos, loop: Map) -> bool:
    if pos in loop:
        return False

    counter = 0
    return symbols


map_test2 = load('test2.txt')
print(is_interior(4j + 10, loop_map(map_test2)))

print(
    sum(
        is_interior(x + y * 1j, loop_map(map_test2))
        for x in range(max(int(p.real) for p in map_test2))
        for y in range(max(int(p.imag) for p in map_test2))
    )
)


map_test3 = load('test3.txt')

print(
    sum(
        is_interior(x + y * 1j, loop_map(map_test3))
        for x in range(max(int(p.real) for p in map_test3))
        for y in range(max(int(p.imag) for p in map_test3))
    )
)
print(
    sum(
        is_interior(x + y * 1j, loop)
        for x in range(max(int(p.real) for p in map))
        for y in range(max(int(p.imag) for p in map))
    )
)

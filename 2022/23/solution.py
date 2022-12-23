from dataclasses import dataclass
from typing import TypeAlias, Self
from collections import defaultdict

Pos: TypeAlias = complex
Dir: TypeAlias = complex

_default_directions = (1j, -1j, -1, 1)

_neighbours_nswe: dict[Pos, set[Pos]] = {
    1j:  {-1 + 1j,  1j,  1 + 1j},
    -1j: {-1 - 1j, -1j,  1 - 1j},
    -1:  {-1 - 1j,  -1, -1 + 1j},
    1:   { 1 - 1j,   1,  1 + 1j},
}


def neighbours_pos(pos: Pos) -> set[Pos]:
    return {
        pos + move
        for dir in _default_directions
        for move in _neighbours_nswe[dir]
    }


def parse_file(filename: str) -> list[Pos]:
    elves_positions = []
    with open(filename) as f:
        for y, row in enumerate(reversed(f.read().splitlines())):
            for x, character in enumerate(row):
                if character == '#':
                    elves_positions.append(x + y * 1j)
    return elves_positions


test = parse_file('test.txt')
print(test)


def elves_to_str(elves_positions: list[Pos]) -> str:
    xs = [int(p.real) for p in elves_positions]
    ys = [int(p.imag) for p in elves_positions]
    rows = []
    for y in range(min(ys), max(ys) + 1):
        rows.append(''.join(
            [
                '#' if (x + y * 1j) in elves_positions else '.'
                for x in range(min(xs), max(xs) + 1)
            ]
        ))
    return '\n'.join(reversed(rows))


def step_1(
    elves_positions: list[Pos], directions: tuple[Dir],
) -> list[Pos]:

    def next_elve_positions(current_pos: Pos) -> Pos:
        # Dont move if alone
        if all(n not in elves_positions for n in neighbours_pos(current_pos)):
            return current_pos

        # Try a dir
        for dir in directions:
            if all(
                current_pos + neighbour_dir not in elves_positions
                for neighbour_dir in _neighbours_nswe[dir]
            ):
                return current_pos + dir
        # Stay
        return current_pos

    return [next_elve_positions(elve_pos) for elve_pos in elves_positions]


def step_2(
    elves_current_pos: list[Pos], elves_wanted_pos: list[Pos]
) -> list[Pos]:
    elves_group_by_next_pos = defaultdict(set)
    for current, wanted in zip(elves_current_pos, elves_wanted_pos):
        elves_group_by_next_pos[wanted].add(current)

    return [
        wanted if len(elves_group_by_next_pos[wanted]) == 1 else current
        for current, wanted in zip(elves_current_pos, elves_wanted_pos)
    ]


def run(elves_positions: list[Pos], steps: int = 10) -> list[Pos]:

    directions = _default_directions
    print("====== Initial pos ======")
    print(elves_to_str(elves_positions))
    for i in range(steps):
        elves_wanted_positions = step_1(elves_positions, directions)
        elves_positions = step_2(elves_positions, elves_wanted_positions)
        directions = directions[1:] + (directions[0],)
        print(f'====== End of round {i} ======')
        print(elves_to_str(elves_positions))

    x = [int(s.real) for s in elves_positions]
    y = [int(s.imag) for s in elves_positions]
    square_size = (max(x) - min(x) + 1) * (max(y) - min(y) + 1)
    return square_size - len(elves_positions)


# print(run(test))
print(run(parse_file('input.txt')))


def part_2(filename: str) -> int:
    elves_positions = parse_file(filename)

    directions = _default_directions
    i = 1
    while True:
        if (i % 100) == 0:
            print(f'Round {i=}')
        elves_wanted_positions = step_1(elves_positions, directions)
        new_elves_positions = step_2(elves_positions, elves_wanted_positions)
        directions = directions[1:] + (directions[0],)
        if elves_positions == new_elves_positions:
            return i
        i += 1
        elves_positions = new_elves_positions
        # print(elves_to_str(elves_positions))


# print(part_2('test.txt'))
print(part_2('input.txt'))

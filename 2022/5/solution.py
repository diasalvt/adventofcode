import re

Crates = list[list[str]]
Move = tuple[int]
Moves = list[tuple[int, Move]]


def parse_file(filename: str) -> tuple[Crates, Moves]:
    with open(filename) as f:
        raw_crates, raw_moves = f.read().split('\n\n')

    def parse_crates(raw_crates: str) -> Crates:
        *raw_crates_rows, numbers = raw_crates.splitlines()
        columns = int(numbers.split()[-1])
        crates = [list() for i in range(columns)]

        for row in raw_crates_rows:
            crates_chars = [c for i, c in enumerate(row) if (i % 4) == 1]
            for i, char in enumerate(crates_chars):
                if char != ' ':
                    crates[i].insert(0, char)

        return crates

    crates = parse_crates(raw_crates)

    def parse_moves(raw_moves: str) -> Moves:
        move_lines = raw_moves.splitlines()
        move_digits = [map(int, re.findall(r'\d+', m)) for m in move_lines]
        return [(quantity, (_from, _to)) for quantity, _from, _to in move_digits]

    moves = parse_moves(raw_moves)

    return crates, moves


crates, moves = parse_file('input.txt')


def move(crates: Crates, move: Move) -> Crates:
    qt, (_from, _to) = move
    _from, _to = _from - 1, _to - 1  # Index to 0

    crates[_to].extend(reversed(crates[_from][-qt:]))
    del crates[_from][-qt:]

    return crates


def test_move():
    crates = [
        ['A', 'B'],
        [],
        ['C']
    ]

    assert move(crates, (2, (1, 3))) == [
        [],
        [],
        ['C', 'B', 'A']
    ]


def play(crates: Crates, moves: Moves, move_fn=move) -> Crates:
    for m in moves:
        print(f'Crates {crates}')
        print(f'Move {m}')
        crates = move_fn(crates, m)

    return [stack[-1] for stack in crates]


# print(''.join(play(crates, moves)))


def move2(crates: Crates, move: Move) -> Crates:
    qt, (_from, _to) = move
    _from, _to = _from - 1, _to - 1  # Index to 0

    crates[_to].extend(crates[_from][-qt:])
    del crates[_from][-qt:]

    return crates


def test_play2():
    crates, moves = parse_file('test.txt')
    assert ''.join(play(crates, moves, move2)) == 'MCD'


print(''.join(play(crates, moves, move_fn=move2)))

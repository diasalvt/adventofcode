from typing import NamedTuple
from collections import defaultdict

Pos = complex
Wind = str
Board = defaultdict[Pos, list[Wind]]


def parse_file(filename: str) -> tuple[Board, tuple[int, int]]:
    with open(filename) as f:
        # drop first and last row
        rows = f.read().splitlines()[1:-1]
        blizzards: Board = defaultdict(list)
        for y, row in enumerate(reversed(rows)):
            for x, character in enumerate(row[1:-1]):
                if character in ['>', '<', '^', 'v']:
                    blizzards[x + y * 1j].append(character)

        return blizzards, (len(rows[0]) - 2, len(rows))


def board_str(board: Board, board_size) -> str:
    size_x, size_y = board_size

    cum_str = ''
    for y in reversed(range(size_y)):
        cum_str += ''.join(
            '#' if x + y * 1j in board else '.' for x in range(size_x)
        ) + '\n'
    return cum_str


blizzard_move = {
    '>': 1,
    '<': -1,
    '^': 1j,
    'v': -1j
}

elve_moves = list(blizzard_move.values()) + [0]


def wrap(pos: Pos, size_x: int, size_y: int) -> Pos:
    return (pos.real % size_x) + (pos.imag % size_y) * 1j


def next_board(board: Board, board_size: tuple[int, int]) -> Board:
    new_board: Board = defaultdict(list)
    for pos, blizzards in board.items():
        for blizzard in blizzards:
            new_board[
                wrap(pos + blizzard_move[blizzard], *board_size)
            ].append(blizzard)
    return new_board


board_test, size_test = parse_file('test.txt')
# print(board_str(board_test, size_test))
# board_test = next_board(board_test, size_test)
# print(board_str(board_test, size_test))
# print(board_str(next_board(board_test, size_test), size_test))


def bfs(
    initial_board: Board, board_size: tuple[int, int], start: Pos, end: Pos
) -> int:

    next_pos = {start}
    current_board = initial_board
    size_x, size_y = board_size

    def is_valid_pos(pos: Pos, board: Board) -> bool:
        if pos in [start, end]:
            return True
        return (
            (0 <= pos.real < size_x) and
            (0 <= pos.imag < size_y) and
            (pos not in board)
        )

    i = 0
    while end not in next_pos:
        current_board = next_board(current_board, board_size)
        _future_next_pos = set()
        for p in next_pos:
            for move in elve_moves:
                if is_valid_pos(p + move, current_board):
                    _future_next_pos.add(p + move)
        next_pos = _future_next_pos
        i += 1

    return i


def part_1(filename: str) -> int:
    board, board_size = parse_file(filename)

    size_x, size_y = board_size
    start = 0 + size_y * 1j
    end = size_x - 1 - 1j

    return bfs(board, board_size, start, end)


print(part_1('test.txt'))
print(part_1('input.txt'))


class State(NamedTuple):
    pos: Pos
    seen: tuple[Pos]


def bfs2(
    initial_board: Board, board_size: tuple[int, int], start: Pos, end: Pos
) -> int:

    next_states = {State(start, tuple())}
    current_board = initial_board
    size_x, size_y = board_size

    def is_valid_pos(pos: Pos, board: Board) -> bool:
        if pos in [start, end]:
            return True
        return (
            (0 <= pos.real < size_x) and
            (0 <= pos.imag < size_y) and
            (pos not in board)
        )

    i = 0
    while State(end, (end, start, end)) not in next_states:
        current_board = next_board(current_board, board_size)
        _future_next_states = set()
        for state in next_states:
            for move in elve_moves:
                p = state.pos + move
                if is_valid_pos(p, current_board):
                    if (p == start) and (state.seen == (end,)):
                        _future_next_states.add(State(p, (end, start)))
                    elif (p == end) and (state.seen in [tuple(), (end, start)]):
                        _future_next_states.add(State(p, state.seen + (end,)))
                    else:
                        _future_next_states.add(State(p, state.seen))
        next_states = _future_next_states
        i += 1

    return i


def part_2(filename: str) -> int:
    board, board_size = parse_file(filename)

    size_x, size_y = board_size
    start = 0 + size_y * 1j
    end = size_x - 1 - 1j

    return bfs2(board, board_size, start, end)


print(part_2('test.txt'))
print(part_2('input.txt'))

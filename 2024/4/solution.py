from typing import TypeAlias
from itertools import product

Pos: TypeAlias = complex
Map: TypeAlias = dict[Pos, str]


def load(filename: str) -> Map:
    board = {}

    with open(filename) as f:
        for y, row in enumerate(f.read().splitlines()):
            for x, char in enumerate(row):
                board[x + y * 1j] = char

    return board


board = load('input.txt')


def get_words_pos(board: Map, pos: Pos, length: int) -> list[str]:
    shifts = set(product({-1, 0, 1}, repeat=2)) - {(0, 0)}
    words = []
    for x_shift, y_shift in shifts:
        word = ''.join(
            board.get((x_shift + y_shift * 1j) * i + pos, '')
            for i in range(length)
        )
        if len(word) == length:
            words.append(word)
    return words


print(sum(get_words_pos(board, pos, 4).count('XMAS') for pos in board))


def get_words_cross(board: Map, pos: Pos) -> list[str]:
    words = []
    for shift in [(-1 - 1j, 0, 1 + 1j), (-1 + 1j, 0, 1 - 1j)]:
        word = ''.join(
            board.get(s + pos, '')
            for s in shift
        )
        if len(word) == 3:
            words.append(word)
    return words


print(
    sum(
        len(
            [
                w
                for w in get_words_cross(board, pos)
                if w in {'MAS', 'SAM'}
            ]
        ) == 2
        for pos in board
    )
)

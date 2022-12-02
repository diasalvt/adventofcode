from itertools import pairwise
from typing import Tuple, List

Move = Tuple[str, str]


def parse_file(filename: str) -> List[Move]:

    def transform(s: str) -> str:
        replacement = {
            'X': 'A',
            'Y': 'B',
            'Z': 'C'
        }

        for k, v in replacement.items():
            s = s.replace(k, v)

        return s

    with open(filename) as f:
        content = f.read().splitlines()
        moves = map(lambda x: tuple(transform(x).split()), content)

    return moves


def parse_file2(filename: str) -> List[Move]:

    with open(filename) as f:
        content = f.read().splitlines()
        moves = map(lambda x: tuple(x.split()), content)

    return moves


moves = parse_file('input.txt')

rules = list(pairwise('ABCA'))  # list of (X, Y) meaning Y greater than X


def score(move: Move) -> int:
    opponent, player = move
    score_char = {c: ord(c) - ord('A') + 1 for c in 'ABC'}

    match move:
        case move if move in rules:
            result = 6
        case (x, y) if x == y:
            result = 3
        case _:
            result = 0

    return score_char[player] + result


def game_score(moves: List[Move]) -> int:
    return sum(map(score, moves))


def test_score():
    assert score(('A', 'A')) == (1 + 3)
    assert score(('A', 'B')) == (2 + 6)
    assert score(('C', 'B')) == (2 + 0)
    assert score(('A', 'C')) == (3 + 0)
    assert score(('C', 'C')) == (3 + 3)


def test_game_score():
    moves = parse_file('test_input.txt')
    assert game_score(moves) == 15


print(game_score(moves))

def game_score2(moves: List[Move]) -> int:
    def score(move: Move) -> int:
        score_char = {c: ord(c) - ord('A') + 1 for c in 'ABC'}

        match move:
            case (a, 'X'):
                return score_char[{y: x for x, y in rules}[a]]
            case (a, 'Y'):
                return score_char[a] + 3
            case (a, 'Z'):
                return score_char[{x: y for x, y in rules}[a]] + 6

    return sum(map(score, moves))

def test_game_score2():
    moves = parse_file2('test_input.txt')
    assert game_score2(moves) == 12

print(game_score2(parse_file2('input.txt')))

from operator import add
from collections import Counter
from itertools import accumulate
from dataclasses import dataclass
from typing import Tuple, Self, Counter, Dict, List
from enum import StrEnum

Move = StrEnum('Move', ['^', 'v', '<', '>'])

@dataclass(eq=True, frozen=True)
class Pos:
    x: int
    y: int

    def __add__(self: Self, other: Self) -> Self:
        return Pos(self.x + other.x, self.y + other.y)

move_effect: Dict[Move, Pos] = {
    Move['^']: Pos(1, 0),
    Move['v']: Pos(-1, 0),
    Move['<']: Pos(0, -1),
    Move['>']: Pos(0, 1)
}

valid_moves = [m.value for m in Move]

class Map:

    def __init__(self: Self):
        self.current_position: Pos = Pos(0, 0)
        self.seen_positions: Counter[Pos] = Counter([self.current_position])

    def play(self: Self, moves: List[Move]) -> Self:
        positions: List[Pos] = list(accumulate(map(lambda x: move_effect[x], moves), add))
        self.seen_positions.update(
            positions
        )
        self.current_position = positions[-1]
        return self

    def count_pos(self: Self) -> int:
        return len(self.seen_positions.keys())

def str_to_move(s: str) -> List[Move]:
    return [Move[x] for x in s if x in valid_moves]

def test_map_move():
    assert Map().play(str_to_move('^v')).count_pos() == 2
    assert Map().play(str_to_move('^>v<')).count_pos() == 4
    assert Map().play(str_to_move('^v^v^v^v^v')).count_pos() == 2

with open('input.txt') as f:
    moves_char = f.read()
    moves: List[Move] = str_to_move(moves_char)

santa_map = Map().play(moves)
print(santa_map.count_pos())

santa_map = Map().play(moves[::2])
robo_map = Map().play(moves[1::2])
print(len(santa_map.seen_positions + robo_map.seen_positions))

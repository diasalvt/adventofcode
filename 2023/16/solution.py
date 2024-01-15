from dataclasses import dataclass
from typing import Any, Self


Pos = tuple[int, int]
Dir = str  # N, S, E, W

DIRS: dict[Dir, tuple[int, int]] = {
    'N': (1, 0),
    'S': (-1, 0),
    'E': (0, 1),
    'W': (0, -1)
}


@dataclass
class Array:
    arr: list[list[Any]]

    height = property(lambda self: len(self.arr))
    width = property(lambda self: len(self.arr[0]))

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls([list(line) for line in s.splitlines()])

    def is_valid_pos(self, pos: Pos) -> bool:
        i, j = pos
        return (0 <= i <= self.height) & (0 <= j <= self.width)

    def neighbours(self, pos: Pos) -> list[Pos]:
        i, j = pos
        return list(filter(
            self.is_valid_pos,
            map(
                lambda x: (x[0] + i, x[1] + j),
                [
                    (-1, 0),
                    (0, -1), (0, 1),
                    (1, 0)
                ]
            )
        ))


@dataclass
class PlayerState:
    pos: Pos = (0, 0)
    dir: Dir


@dataclass
class GameState:
    array: Array
    players: list[PlayerState]
    past_players_states: set[PlayerState]

    def move_player(self, player: PlayerState) -> list[PlayerState]:
        i, j = player.pos
        shift_i, shift_j = player.dir
        next_pos = (i + shift_i, j + shift_j)
        if self.array.is_valid(next_pos):

        return [type(self)(self.array, pos) for pos in next_pos]


terrain = Array.from_str(open('test.txt').read())
print(terrain)
w = Walk(terrain)
print(w)
print(next(w))
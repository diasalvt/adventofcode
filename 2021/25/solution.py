from itertools import product
from select import POLLRDHUP
from typing import *
from dataclasses import dataclass

Pos = Tuple[int, int]

@dataclass
class Board:
    size: Tuple[int, int]
    horizontal_blobs: Set[Pos]
    vertical_blobs: Set[Pos]

    @classmethod
    def from_file(cls, filename: str) -> 'Board':
        h_blobs: Set[Pos] = set()
        v_blobs: Set[Pos] = set()

        _c_blobs = {'>': h_blobs, 'v': v_blobs}
        with open(filename) as f:
            for i, row in enumerate(f):
                for j, character in enumerate(row.strip()):
                    if character != '.':
                        _c_blobs[character].add((i, j))
        
        return cls((i + 1, j + 1), h_blobs, v_blobs)

    def __repr__(self) -> None:
        repr = ""
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if (i, j) in self.horizontal_blobs:
                    repr += '>'
                elif (i, j) in self.vertical_blobs:
                    repr += 'v'
                else:
                    repr += '.'
            repr += '\n'
        return repr

    def move(self, dir: str, pos: Pos) -> Pos:
        i, j = pos
        max_i, max_j = self.size

        if dir == '>':
            return (i, j+1) if j < (max_j - 1) else (i, 0)
        elif dir == 'v':
            return (i+1, j) if i < (max_i - 1) else (0, j)
        else:
            raise ValueError(f'{dir} is not a valid direction')

    def next_pos(self, dir: str, pos: Pos) -> bool:
        i, j = pos
        next_pos = self.move(dir, pos)

        if (next_pos in self.horizontal_blobs) or (next_pos in self.vertical_blobs):
            return (pos, False)
        return (next_pos, True)

    def step(self) -> bool:
        h_blobs = {self.next_pos('>', blob) for blob in self.horizontal_blobs}
        blobs, h_has_changed = zip(*h_blobs)
        self.horizontal_blobs = set(blobs)
        v_blobs = {self.next_pos('v', blob) for blob in self.vertical_blobs}
        blobs, v_has_changed = zip(*v_blobs)
        self.vertical_blobs = set(blobs)

        return any(h_has_changed) or any(v_has_changed)

board = Board.from_file('input25.txt')
print(board)
i = 1
while board.step():
    i += 1
print(i)

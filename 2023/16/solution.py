from dataclasses import dataclass
from typing import Any, Self, Generator


Pos = tuple[int, int]


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

    def __iter__(self) -> Generator:

@dataclass
class Walk:
    array: Array
    curr: Pos = (0, 0)

    def __next__(self) -> list[Self]:
        i, j = self.curr
        next_pos = filter(
            self.array.is_valid_pos,
            map(
                lambda x: (x[0] + i, x[1] + j),
                [
                    (-1, 0),
                    (0, -1), (0, 1),
                    (1, 0)
                ]
            )
        )

        return [type(self)(self.array, pos) for pos in next_pos]


terrain = Array.from_str(open('test.txt').read())
print(terrain)
w = Walk(terrain)
print(w)
print(next(w))
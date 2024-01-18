from dataclasses import dataclass
from queue import PriorityQueue
from typing import Self

Map = tuple[dict[complex, int], int, int]


@dataclass
class Map:
    data: dict[complex, int]
    height: int
    width: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        data = s.splitlines()
        height = len(data)
        width = len(data[0])
        return cls(
            {
                complex(i, j): c
                for i, row in enumerate(data)
                for j, c in enumerate(row)
            },
            height, width
        )

    def is_valid(self, pos: complex) -> bool:
        i, j = pos.real, pos.imag
        return (0 < i < self.height) and (0 < j < self.width)

    def load(filename: str) -> Map:
    return Map.from_str(open(filename).read())


test = load('test.txt')
print(test)


@dataclass(frozen=True)
class State:
    pos: complex
    nb_steps: int
    dir: complex

    def neighbours(self, map: Map, max_steps: int) -> list[Self]:
        forbidden_dirs = (
            {-self.dir} |  # Do not go back
            {self.dir} if nb_steps == max_steps else {}  # Do not go forward
        )

        return [
            State(pos + dir, nb_steps + 1 if nb_steps < max_steps else 1, dir)
            for dir in {-1, 1, -1j, j} - forbidden_dirs
            if map.is_valid(pos + dir)
        ]


def shortest_path(map: Map, max_steps: int = 3) -> int:
    min_cost: defaultdict[State, int] = defaultdict(lambda: math.inf)

    to_explore = PriorityQueue()
    to_explore.put((0, (0, 1)))
    min_cost[0] = {(0, 1): 0}

    while to_explore:
        curr = to_explore.pop()

        for next_state in curr.neighbours(map, max_steps):
            new_cost = min_cost[curr.pos] + map[next_state.pos]
            if new_cost < min_cost[next_state.pos]:
                min_cost[next_state] = new_cost

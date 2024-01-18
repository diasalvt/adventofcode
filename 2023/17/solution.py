from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Self
from collections import defaultdict
import math

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
                complex(i, j): int(c)
                for i, row in enumerate(data)
                for j, c in enumerate(row)
            },
            height, width
        )

    def is_valid(self, pos: complex) -> bool:
        i, j = pos.real, pos.imag
        return (0 <= i < self.height) and (0 <= j < self.width)

    def __getitem__(self, key: complex) -> int:
        return self.data[key]


def load(filename: str) -> Map:
    return Map.from_str(open(filename).read())


map = load('input.txt')


@dataclass(frozen=True)
class State:
    pos: complex
    nb_steps: int
    dir: complex

    def neighbours(
        self, map: Map, min_steps: int, max_steps: int
    ) -> list[Self]:
        forbidden_dirs = {-self.dir}  # Dont go back

        if self.nb_steps == max_steps:
            forbidden_dirs |= {self.dir}
        if self.nb_steps < min_steps:
            forbidden_dirs |= {1j/self.dir, -1j/self.dir}

        return [
            type(self)(
                self.pos + dir,
                self.nb_steps + 1 if dir == self.dir else 1,
                dir
            )
            for dir in {-1, 1, -1j, 1j} - forbidden_dirs
            if map.is_valid(self.pos + dir)
        ]


@dataclass(order=True)
class PrioritizedState:
    priority: int
    state: State = field(compare=False)


def shortest_path(
    map: Map, min_steps: int = 0, max_steps: int = 3
) -> int:
    min_cost: defaultdict[State, int] = defaultdict(lambda: math.inf)

    to_explore = PriorityQueue()
    to_explore.put(PrioritizedState(0, State(0, 0, 1)))
    to_explore.put(PrioritizedState(0, State(0, 0, 1j)))

    while not to_explore.empty():
        item = to_explore.get_nowait()
        cost, curr = item.priority, item.state

        for next_state in curr.neighbours(map, min_steps, max_steps):
            new_cost = cost + map[next_state.pos]
            if new_cost < min_cost[next_state]:
                min_cost[next_state] = new_cost
                to_explore.put(PrioritizedState(new_cost, next_state))

    return min_cost


print(
    min(
        cost
        for state, cost in shortest_path(map).items()
        if state.pos == map.width - 1 + (map.height - 1) * 1j
    )
)
print(
    min(
        cost
        for state, cost in shortest_path(map, 4, 10).items()
        if state.pos == map.width - 1 + (map.height - 1) * 1j
    )
)

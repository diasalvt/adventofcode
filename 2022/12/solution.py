from dataclasses import dataclass
import heapq
from typing import Optional
from itertools import permutations


Pos = tuple[int, int]
ElevationMap = list[list[int]]


@dataclass
class Grid:
    elevation: ElevationMap
    height: int
    width: int
    start_pos: Pos
    end_pos: Pos

    @classmethod
    def from_list(cls, l: list[list[int]]) -> 'Grid':
        height, width = len(l), len(l[0])
        for i in range(height):
            for j in range(width):
                match l[i][j]:
                    case 'S':
                        start_pos = (i, j)
                        l[i][j] = 'a'
                    case 'E':
                        end_pos = (i, j)
                        l[i][j] = 'z'
                l[i][j] = ord(l[i][j]) - ord('a')

        return cls(l, height, width, start_pos, end_pos)

    def in_grid(self, p: Pos) -> bool:
        x, y = p
        return (0 <= x < self.height) and (0 <= y < self.width)

    def __repr__(self) -> str:
        return f'Grid({self.start_pos=}{self.end_pos=}{self.elevation[:2]=})'


def parse_file(filename: str) -> Grid:
    with open(filename) as f:
        return Grid.from_list([list(row) for row in f])


test = parse_file('test.txt')
grid = parse_file('input.txt')
# print(test)


def neighbours(p: Pos, g: Grid) -> set[Pos]:
    x, y = p
    curr = g.elevation[x][y]
    next_to = {
        (x + n_x, y + n_y)
        for n_x, n_y in {(-1, 0), (1, 0), (0, -1), (0, 1)}
    }

    return {
        (x, y)
        for x, y in next_to
        if g.in_grid((x, y)) and ((g.elevation[x][y] - curr) <= 1)
    }


Node = tuple[int, Pos, Optional[Pos]]  # Cost, Pos, PrevPos


def _show(grid: Grid, queue: list, seen):
    x, y = grid.height, grid.width
    for i in range(x):
        line = []
        for j in range(y):
            if (i, j) in queue:
                line.append('#')
            elif (i, j) in seen:
                line.append('-')
            else:
                line.append('.')
        print(''.join(line))
    print('\n')


def shortest_path(grid: Grid) -> dict[Pos, Pos]:
    to_see = [(0, grid.start_pos, None)]
    heapq.heapify(to_see)
    seen = set()
    path = {}
    cost_node = {}

    while grid.end_pos not in seen:
        cost, closest_pos, closest_prev_pos = heapq.heappop(to_see)
        seen |= {closest_pos}
        path[closest_pos] = closest_prev_pos
        for x in (neighbours(closest_pos, grid) - seen):
            if x not in cost_node or (cost_node[x] > (cost + 1)):
                heapq.heappush(to_see, (cost + 1, x, closest_pos))
                cost_node[x] = cost + 1

    return path


def list_path(end_pos: Pos, path: dict[Pos, Pos]) -> list[Pos]:
    node = end_pos
    res = [node]
    while node:
        res.append(node := path[node])
    return list(reversed(res))[2:]  # Remove start and None (start antecedent)


def test_shortest_path():
    assert len(list_path(test.end_pos, shortest_path(test))) == 31


print(len(list_path(grid.end_pos, shortest_path(grid))))

"""
    Change Order: start from end and stop when elevation 'a' is found
    - adjust possible neighbours
"""

def neighbours2(p: Pos, g: Grid) -> set[Pos]:
    x, y = p
    curr = g.elevation[x][y]
    next_to = {
        (x + n_x, y + n_y)
        for n_x, n_y in {(-1, 0), (1, 0), (0, -1), (0, 1)}
    }

    return {
        (x, y)
        for x, y in next_to
        if g.in_grid((x, y)) and ((g.elevation[x][y] - curr) >= -1)
    }


def shortest_path2(grid: Grid) -> dict[Pos, Pos]:
    to_see = [(0, grid.end_pos, None)]
    heapq.heapify(to_see)
    seen = set()
    val_seen = set()
    path = {}
    cost_node = {}

    while 0 not in val_seen:
        cost, closest_pos, closest_prev_pos = heapq.heappop(to_see)
        seen |= {closest_pos}
        x, y = closest_pos
        val_seen |= {grid.elevation[x][y]}
        path[closest_pos] = closest_prev_pos
        for x in (neighbours2(closest_pos, grid) - seen):
            if x not in cost_node or (cost_node[x] > (cost + 1)):
                heapq.heappush(to_see, (cost + 1, x, closest_pos))
                cost_node[x] = cost + 1

    return path


positions = shortest_path2(grid)
start_pos = next(k for k, v in positions.items() if grid.elevation[k[0]][k[1]] == 0)
print(len(list_path(start_pos, positions)))

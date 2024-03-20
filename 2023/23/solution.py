from functools import cache
from collections import deque, defaultdict

Pos = complex
Dir = complex

_directions = {
    '>': 1,
    '<': -1,
    '^': -1j,
    'v': 1j
}

Plan = tuple[set[Pos], dict[Pos, Dir]]


def load(filename: str) -> Plan:
    positions = set()
    forced_dir = {}

    with open(filename) as f:
        for i, row in enumerate(f):
            for j, c in enumerate(row):
                pos = j + i * 1j
                if c == '.':
                    positions.add(pos)
                if c in _directions:
                    positions.add(pos)
                    forced_dir[pos] = _directions[c]

    return positions, forced_dir


def neighbours(plan: Plan, current_pos: Pos) -> set[Pos]:
    positions, forced_dir = plan

    possible_dirs = (
        {forced_dir[current_pos]}
        if current_pos in forced_dir
        else {1, -1, 1j, -1j}
    )

    return {
        current_pos + dir
        for dir in possible_dirs
        if (current_pos + dir) in positions
    }


test_plan = load('test.txt')
plan = load('input.txt')


def longest_path(plan: Plan) -> int:

    start = next(p for p in plan[0] if p.imag == 0)
    end = next(
        p 
        for p in plan[0]
        if p.imag == max(p.imag for p in plan[0])
    )

    @cache
    def rec_longest_path(current_pos: Pos, seen: frozenset[Pos]) -> int:
        if current_pos == end:
            return 1

        next_pos = neighbours(plan, current_pos) - seen
        steps = 1
        while len(next_pos) == 1:
            current_pos = next_pos.pop()
            seen |= {current_pos}
            if current_pos == end:
                return steps
            next_pos = neighbours(plan, current_pos) - seen
            steps += 1

        neighbours_longest_path = (
            filter(
                lambda x: x >= 0,
                map(
                    lambda x: rec_longest_path(x, seen | {x}),
                    next_pos
                )
            )
        )

        return max(
           (n + steps for n in neighbours_longest_path),
           default=-1
        )

    return rec_longest_path(start, frozenset({start}))


print(longest_path(plan))
positions, forced_dirs = plan

# Too slow
# print(longest_path((positions, {})))


def is_node(plan: Plan, pos: Pos) -> bool:
    return len(neighbours(plan, pos)) > 2


Graph = dict[Pos, dict[Pos, int]]


def bfs_next_node(plan: Plan, start: Pos, special_nodes: set[Pos]) -> int:

    states_to_explore = deque([(0, start, set())])
    nodes_distance = defaultdict(int)

    while states_to_explore:
        length, pos, seen = states_to_explore.popleft()

        if pos != start and pos in special_nodes:
            if length > nodes_distance[pos]:
                nodes_distance[pos] = length
        else:
            for n in neighbours(plan, pos) - seen:
                states_to_explore.append((length + 1, n, seen | {pos}))

    return nodes_distance


def build_graph(plan: Plan) -> Graph:
    start = next(p for p in plan[0] if p.imag == 0)
    end = next(
        p
        for p in plan[0]
        if p.imag == max(p.imag for p in plan[0])
    )

    nodes = (
        {start, end} |
        {p for p in plan[0] if is_node(plan, p)}
    )

    return {
        n: bfs_next_node(plan, n, nodes)
        for n in nodes
    }


def longest_path_graph(g: Graph, start: Pos, end: Pos):
    states_to_explore = deque([(0, start, set())])

    max_length = 0
    while states_to_explore:
        length, pos, seen = states_to_explore.popleft()

        if pos == end:
            if length > max_length:
                max_length = length
        else:
            for next_pos, dist in g[pos].items():
                if next_pos not in seen:
                    states_to_explore.append(
                        (length + dist, next_pos, seen | {pos})
                    )

    return max_length


def solve(plan: Plan) -> int:
    start = next(p for p in plan[0] if p.imag == 0)
    end = next(
        p
        for p in plan[0]
        if p.imag == max(p.imag for p in plan[0])
    )
    graph = build_graph(plan)
    return longest_path_graph(graph, start, end)


positions, _ = plan
print(solve((positions, {})))

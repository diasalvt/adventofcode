from functools import cache
from collections import deque

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


def bfs(plan: Plan) -> int:
    start = next(p for p in plan[0] if p.imag == 0)
    end = next(
        p
        for p in plan[0]
        if p.imag == max(p.imag for p in plan[0])
    )

    states_to_explore = deque([(0, start, (-1, set()))])
    max_length = 0
    i = 0
    while states_to_explore:
        length, pos, (prev_pos, seen_nodes) = states_to_explore.popleft()
        print(i := i + 1)

        # Test if we can beat the current max_length
        # if (length + len(plan[0] - seen)) > max_length:
        if pos == end:
            if length > max_length:
                max_length = length
        else:
            seen = {prev_pos} + seen_nodes
            for n in neighbours(plan, pos) - seen:
                if is_node(plan, pos):
                    seen_nodes |= {prev_pos}
                states_to_explore.append((length + 1, n, (prev_pos, seen_nodes)))

    return max_length


print(bfs(test_plan))

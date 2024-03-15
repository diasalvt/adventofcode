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
                pos = i + j * 1j
                if c == '.':
                    positions.add(pos)
                if c in _directions:
                    positions.add(pos)
                    forced_dir[pos] = _directions[c]

    return positions, forced_dir


def neighbours(plan: Plan, current_pos: Pos) -> set[Pos]:
    positions, forced_dir = plan

    possible_dirs = (
        forced_dir[current_pos]
        if current_pos in forced_dir
        else {1, -1, 1j, -1j}
    )

    return {
        current_pos + dir
        for dir in possible_dirs
        if (current_pos + dir) in plan
    }


test_plan, test_forced_dir = load('test.txt')
plan = load('input.txt')
print(test_plan)


def longest_path(plan: Plan) -> int:
    if pos == 

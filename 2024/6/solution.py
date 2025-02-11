Pos = complex
Dir = complex
Elem = str
Plan = dict[Pos, Elem]
Guard = tuple[Pos, Dir]


def load(filename: str) -> tuple[Plan, Pos]:
    start = 0
    with open(filename) as f:
        plan = {}
        for j, row in enumerate(f.read().splitlines()):
            for i, c in enumerate(row):
                plan[i - j * 1j] = c
                if c == '^':
                    start = i - j * 1j
    return plan, (start, 1j)


plan, start = load('input.txt')


def step(plan: Plan, guard: Guard) -> Guard:
    pos, dir = guard
    if plan.get(pos + dir, '') == '#':
        dir = -dir * 1j
        return pos, dir
    else:
        return pos + dir, dir


def play(plan: Plan, guard: Guard) -> int:
    seen_guards = set()
    while (guard[0] in plan) and not(guard in seen_guards):
        seen_guards |= {guard}
        guard = step(plan, guard)

    return len(set(pos for pos, _ in seen_guards)), guard in seen_guards


print(play(plan, start)[0])


def part2(plan: Plan, guard: Guard) -> int:
    res = 0
    for pos in filter(lambda x: plan[x] == '.', plan):
        plan[pos] = '#'
        if play(plan, guard)[1]:
            res += 1
        plan[pos] = '.'
    return res


print(part2(plan, start))

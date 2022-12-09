from itertools import chain, repeat, accumulate, product

Cmd = tuple[str, int]
Pos = tuple[int, int]


def parse_file(filename: str) -> list[Cmd]:
    with open(filename) as f:
        return [
            (dir, int(count)) for dir, count in map(lambda x: x.split(), f)
        ]


def direction(dir: str) -> Pos:
    match dir:
        case 'R':
            return (0, 1)
        case 'L':
            return (0, -1)
        case 'U':
            return (1, 0)
        case 'D':
            return (-1, 0)
        case _:
            raise ValueError(f'{dir} is not a valid direction (RLUD)')


def expand_cmds(cmds: list[Cmd]) -> list[str]:
    return map(
        direction,
        chain.from_iterable(repeat(dir, count) for dir, count in cmds)
    )


cmds = parse_file('test.txt')
print(list(expand_cmds(cmds)))


def add(p1: Pos, p2: Pos) -> Pos:
    (x1, y1), (x2, y2) = p1, p2
    return (x1 + x2, y1 + y2)


def sub(p1: Pos, p2: Pos) -> Pos:
    (x1, y1), (x2, y2) = p1, p2
    return (x1 - x2, y1 - y2)


def neg(p: Pos) -> Pos:
    x, y = p
    return (-x, -y)


def is_next_to(p1: Pos, p2: Pos) -> bool:
    return max(map(abs, sub(p1, p2))) <= 1


def full_neighbours(p: Pos) -> set[Pos]:
    return {
        add(p, dir)
        for dir in product([-1, 0, 1], [-1, 0, 1])
        if dir != 0
    }


def cross_neighbours(p: Pos) -> set[Pos]:
    return {
        add(p, dir)
        for dir in {(-1, 0), (0, -1), (1, 0), (0, 1)}
    }


def play(cmds: list[Cmd]) -> set[Pos]:
    directions = expand_cmds(cmds)
    pos_head, pos_tail = (0, 0), (0, 0)
    pos_seen: set[Pos] = {pos_tail}

    for dir in directions:
        # Move Head
        prev_pos_head = pos_head
        pos_head = add(pos_head, dir)
        if not is_next_to(pos_head, pos_tail):
            pos_tail = prev_pos_head
            pos_seen |= {pos_tail}

    return pos_seen


def test_play():
    cmds = parse_file('test.txt')
    assert len(play(cmds)) == 13


cmds = parse_file('input.txt')
print(len(play(cmds)))


def play2(cmds: list[Cmd], size: int = 10) -> set[Pos]:
    directions = expand_cmds(cmds)
    pos_knots = [(0, 0)]*size
    pos_seen: set[Pos] = {pos_knots[-1]}

    def move_adjacent(
        p1: Pos, p2: Pos
    ) -> Pos:
        """
            Compute new p2, following p1
        """
        if not is_next_to(p1, p2):
            cross_p1 = cross_neighbours(p1)
            full_p1 = full_neighbours(p1)
            full = full_neighbours(p2)
            if len(r := full & cross_p1) > 0:
                return r.pop()
            else:
                return (full & full_p1).pop()
        return p2

    for dir in directions:
        pos_knots[0] = add(pos_knots[0], dir)
        pos_knots = list(accumulate(
            pos_knots,
            move_adjacent)
        )
        pos_seen |= {pos_knots[-1]}

    return pos_seen


def show_map(pos_seen: set[Pos]) -> None:
    x, y = zip(*pos_seen)
    for i in range(min(x), max(x) + 1):
        line = ''.join(
            [
                '#' if (i, j) in pos_seen else '.'
                for j in range(min(y), max(y) + 1)
            ]
        )
        print(line)


show_map(play2(parse_file('test2.txt')))
print(len(play2(parse_file('input.txt'))))

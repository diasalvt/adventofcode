from functools import reduce

Pos = complex
Type = str
Terrain = dict[Pos, Type]
Command = complex


def load(filename: str) -> tuple[Terrain, list[Command]]:
    str_to_dir = {
        'v': 1j,
        '^': -1j,
        '<': -1,
        '>': 1
    }

    with open(filename) as f:
        terrain_str, commands_str = f.read().split('\n\n')
        terrain = {
            x + 1j * y: c
            for y, row in enumerate(terrain_str.splitlines())
            for x, c in enumerate(row)
        }
        commands = [
            str_to_dir[c] for c in commands_str if c in str_to_dir.keys()
        ]
    return terrain, commands


terrain, commands = load('input.txt')


def move(
    p: Pos, command: Command, terrain: Terrain
) -> tuple[bool, terrain]:
    def swap(p1: Pos, p2: Pos, terrain: Terrain) -> Terrain:
        new_terrain = {**terrain}
        new_terrain[p1], new_terrain[p2] = new_terrain[p2], new_terrain[p1]
        return new_terrain

    next_p = p + command
    if terrain[next_p] == '#':
        return False, terrain

    match terrain[next_p]:
        case '#':
            return False, terrain
        case '.':
            return True, swap(p, next_p, terrain)
        case 'O':
            can_move, new_terrain = move(next_p, command, terrain)
            if can_move:
                return True, swap(p, next_p, new_terrain)
            else:
                return False, terrain
        case '[' | ']':
            if command in {1j, -1j}:
                shift = (1 if terrain[next_p] == '[' else -1)

                can_move_left, new_terrain = move(next_p, command, terrain)
                can_move_right, new_terrain = move(
                    next_p + shift,
                    command,
                    new_terrain
                )
                if can_move_left and can_move_right:
                    return True, swap(p, next_p, new_terrain)
                else:
                    return False, terrain
            else:
                can_move, new_terrain = move(next_p, command, terrain)
                if can_move:
                    return True, swap(p, next_p, new_terrain)
                else:
                    return False, terrain


def display(terrain: Terrain) -> None:
    max_x = max(int(k.real) for k in terrain.keys())
    max_y = max(int(k.imag) for k in terrain.keys())

    for y in range(max_y + 1):
        row = ''.join(terrain[x + 1j * y] for x in range(max_x + 1))
        print(row)


def score(terrain: Terrain) -> int:
    return int(sum(
        p.real + 100 * p.imag
        for p, terrain_type in terrain.items()
        if terrain_type in {'O', '['}
    ))


def play(terrain: Terrain, commands: list[Command]) -> terrain:
    pos = {v: k for k, v in terrain.items()}['@']

    for c in commands:
        can_move, terrain = move(pos, c, terrain)
        if can_move:
            pos += c

    return terrain


print(score(play(terrain, commands)))


def wide_terrain(terrain: Terrain) -> Terrain:
    new_terrain = {}
    for p, t in terrain.items():
        new_t = {
            '.': '..',
            '#': '##',
            '@': '@.',
            'O': '[]'
        }[t]
        new_terrain[2*p.real + 1j * p.imag] = new_t[0]
        new_terrain[2*p.real + 1j * p.imag + 1] = new_t[1]
    return new_terrain


print(score(play(wide_terrain(terrain), commands)))

from itertools import pairwise, chain
import matplotlib.pyplot as plt

Pos = tuple[int, ...]


def load(filename: str) -> list[Pos]:
    with open(filename) as f:
        return [tuple(map(int, r.split(','))) for r in f]


positions = load('test.txt')

result = max(
    (abs(p1_x - p2_x) + 1) * (abs(p1_y - p2_y) + 1)
    for p1_x, p1_y in positions
    for p2_x, p2_y in positions
    if (p1_x, p1_y) < (p2_x, p2_y)
)

print(result)


def gen_line(p1: Pos, p2: Pos) -> list[Pos]:
    if p1[0] == p2[0]:
        if p2[1] < p1[1]:
            return [(p1[0], y) for y in reversed(range(p2[1] + 1, p1[1] + 1))]
        else:
            return [(p1[0], y) for y in range(p1[1], p2[1])]
    else:
        if p2[0] < p1[0]:
            return [(x, p1[1]) for x in reversed(range(p2[0] + 1, p1[0] + 1))]
        else:
            return [(x, p1[1]) for x in range(p1[0], p2[0])]


def rectangle(p1: Pos, p2: Pos) -> list[Pos]:
    p1_x, p1_y = p1
    p2_x, p2_y = p2
    corner_1 = p1_x, p2_y
    corner_2 = p2_x, p1_y
    return (
        gen_line(p1, corner_1) + gen_line(corner_1, p2) +
        gen_line(p2, corner_2) + gen_line(corner_2, p1)
    )


segments = list(pairwise(positions + [positions[0]]))
border = list(
    chain.from_iterable(
        gen_line(*s)
        for s in segments
    )
)
border_with_direction = {
    complex(*p): complex(*next_p) - complex(*p)
    for p, next_p in zip(border, border[1:] + [border[0]])
}


def rectangle_is_interior(p1: Pos, p2: Pos, border_with_direction):
    rec = [complex(*p) for p in rectangle(p1, p2)]
    directions = [
        next_p - p
        for p, next_p in zip(rec, rec[1:] + [rec[0]])
    ]

    terrain_rectangle = [
        (border_with_direction[p], d) if p in border_with_direction else (None, d)
        for p, d in zip(rec, directions)
    ]

    block = [
        (((dir / prev_dir) != 1j) and ((terrain_dir / prev_dir) == 1j))
        for (_, prev_dir), (terrain_dir, dir) in pairwise(terrain_rectangle)
        if terrain_dir is not None
    ]
    print(terrain_rectangle)
    print(block)
    return not any(block)


for p1, p2 in segments:
    x_coord, y_coord = zip(p1, p2)
    plt.plot(x_coord, y_coord)

plt.show()

# result = max(
#     ((abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1), p1, p2)
#     for p1 in positions for p2 in positions
#     if (p1 < p2) and rectangle_is_interior(p1, p2, border_with_direction)
# )

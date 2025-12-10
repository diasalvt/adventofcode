Pos = tuple[int, int]


def load(filename: str) -> list[Pos]:
    with open(filename) as f:
        return [tuple(map(int, r.split(','))) for r in f]


positions = load('input.txt')

result = max(
    (abs(p1_x - p2_x) + 1) * (abs(p1_y - p2_y) + 1)
    for p1_x, p1_y in positions
    for p2_x, p2_y in positions
    if (p1_x, p1_y) < (p2_x, p2_y)
)

print(result)

from itertools import pairwise
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

Segment = tuple[Pos, ...]
Segments = list[Segment]


def is_horizontal(s: Segment) -> bool:
    return s[0][1] == s[1][1]


def intersect(s1: Segment, s2: Segment) -> bool:
    # sort
    s1 = tuple(sorted(s1))
    s2 = tuple(sorted(s2))

    # same direction
    if not (is_horizontal(s1) ^ is_horizontal(s2)):
        return False

    h_p1, h_p2 = s1 if is_horizontal(s1) else s2
    v_p1, v_p2 = s1 if (h_p1, h_p2) == s2 else s2

    return (
        (h_p1[1] in range(v_p1[1] + 1, v_p2[1])) and
        (v_p1[0] in range(h_p1[0] + 1, h_p2[0]))
    )


def find_intersections(s: Segment, segments: Segments) -> set[Segment]:
    return {
        segment
        for segment in segments
        if intersect(s, segment)
    }


def points_below(p: Pos, positions: list[Pos]) -> set[Pos]:
    return {
        other_p
        for other_p in positions
        if (p[0] == other_p[0]) and (p[1] < other_p[1])
    }


def rectangle_is_interior(p1: Pos, p2: Pos, segments: Segments):
    corners = [
        p1, (p1[0], p2[1]),
        p2, (p2[0], p1[1])
    ]

    all_corners_inside = all(
        (p in positions) or ((len(points_below(p, positions)) % 2) == 1)
        for p in corners
    )
    sides = list(pairwise(corners + [corners[0]]))
    all_sides_inside = all(
        len(find_intersections(s, segments)) < 1
        for s in sides
    )

    return all_corners_inside and all_sides_inside


segments = list(pairwise(positions + [positions[0]]))

result = max(
    (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
    for p1 in positions for p2 in positions if (p1 < p2) and rectangle_is_interior(p1, p2, segments) )

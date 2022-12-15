import re
from typing import Optional, TypeAlias

Pos: TypeAlias = tuple[int, int]
Range: TypeAlias = tuple[int, int]


def parse_file(filename: str) -> list[tuple[Pos, Pos]]:
    with open(filename) as f:
        return [
            ((s_x, s_y), (b_x, b_y))
            for s_x, s_y, b_x, b_y in map(
                lambda x: map(int, re.findall(r'\d+', x)),
                f.read().splitlines()
            )
        ]


sensor_beacon = parse_file('test.txt')


def dist(p1, p2):
    p1_x, p1_y = p1
    p2_x, p2_y = p2
    return abs(p1_x - p2_x) + abs(p1_y - p2_y)


def intersect_row(sensor, beacon, row):
    s_x, s_y = sensor
    d = dist(sensor, beacon)
    delta_range = (d - abs(s_y - row))
    if delta_range < 0:
        return None
    return (int(s_x - delta_range), int(s_x + delta_range))


def and_range(
    r1: Range, r2: Range
) -> Optional[Range]:
    r1_a, r1_b = r1
    r2_a, r2_b = r2
    inter_a, inter_b = max(r1_a, r2_a), min(r1_b, r2_b)
    if inter_a > inter_b:
        return None
    else:
        return inter_a, inter_b


def size(r) -> int:
    if r is None:
        return 0
    else:
        return r[1] - r[0] + 1


def measure_union(ranges: list[Range]) -> int:
    match ranges:
        case []:
            return 0
        case [a, *other]:
            return (
                size(a) +
                measure_union(other) -
                measure_union(
                    list(filter(
                        lambda x: x is not None,
                        [and_range(a, r) for r in other])
                    ))
            )


def non_present_beacon(sensor_beacon: list[tuple[Pos, Pos]], row: int):
    ranges = list(filter(
        lambda x: x is not None,
        [intersect_row(sensor, beacon, row)
         for sensor, beacon in sensor_beacon]
    ))

    print(ranges)
    size_union_ranges = measure_union(ranges)

    # a beacon in the row is necessarly in the union
    # because he is in the sensing area of some sensor
    beacon_in_union = set(
        beacon_x for _, (beacon_x, beacon_y) in sensor_beacon if beacon_y == row
    )
    return size_union_ranges - len(beacon_in_union)


print(sensor_beacon)
print(non_present_beacon(sensor_beacon, row=10))
sensor_beacon = parse_file('input.txt')
print(sensor_beacon)
print(non_present_beacon(sensor_beacon, row=2_000_000))

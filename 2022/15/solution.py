import re
from typing import Optional, TypeAlias
from functools import lru_cache
import tqdm

Pos: TypeAlias = tuple[int, int]
Range: TypeAlias = tuple[int, int]


def parse_file(filename: str) -> list[tuple[Pos, Pos]]:
    with open(filename) as f:
        return [
            ((s_x, s_y), (b_x, b_y))
            for s_x, s_y, b_x, b_y in map(
                lambda x: map(int, re.findall(r'-?\d+', x)),
                f.read().splitlines()
            )
        ]


sensor_beacon = parse_file('test.txt')


def dist(p1, p2):
    p1_x, p1_y = p1
    p2_x, p2_y = p2
    return abs(p1_x - p2_x) + abs(p1_y - p2_y)


def test_dist():
    assert dist((0, 4), (0, 10)) == 6
    assert dist((1, 4), (0, 10)) == 7


def intersect_row(sensor, beacon, row):
    s_x, s_y = sensor
    d = dist(sensor, beacon)
    delta_range = (d - abs(s_y - row))
    if delta_range < 0:
        return None
    return (int(s_x - delta_range), int(s_x + delta_range))


def test_intersect_row():
    assert intersect_row((1, 4), (0, 10), 5) == (-5, 7)


def and_range(
    r1: Range, r2: Range
) -> Optional[Range]:
    if (r1 is None) or (r2 is None):
        return None
    r1_a, r1_b = r1
    r2_a, r2_b = r2
    inter_a, inter_b = max(r1_a, r2_a), min(r1_b, r2_b)
    if inter_a > inter_b:
        return None
    else:
        return inter_a, inter_b


def test_and_range():
    assert and_range((4, 5), (5, 10)) == (5, 5)
    assert and_range((4, 5), (6, 10)) is None
    assert and_range((6, 10), (4, 5)) is None
    assert and_range((6, 10), (8, 30)) == (8, 10)


def size(r) -> int:
    if r is None:
        return 0
    else:
        return r[1] - r[0] + 1


def test_size():
    assert size((4, 5)) == 2
    assert size((5, 5)) == 1


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


def test_measure_union():
    assert measure_union(
        [
            (5, 10),
            (4, 11),
            (-3, -1),
            (2, 7)
        ]
    ) == 13


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
        beacon_x
        for _, (beacon_x, beacon_y) in sensor_beacon if beacon_y == row
    )
    return size_union_ranges - len(beacon_in_union)


def test_non_present_beacon():
    assert non_present_beacon(parse_file('test.txt'), 10) == 26


sensor_beacon = parse_file('input.txt')
# print(sensor_beacon)
print(non_present_beacon(sensor_beacon, row=2_000_000))


def part_2(sensor_beacon: list[tuple[Pos, Pos]], limit: int):
    for row in tqdm.tqdm(reversed(range(limit))):
        ranges = list(filter(
            lambda x: x is not None,
            [intersect_row(sensor, beacon, row)
             for sensor, beacon in sensor_beacon]
        ))

        size_union_ranges = measure_union(
            [and_range(r, (0, limit)) for r in ranges]
        )
        if size_union_ranges < size((0, limit)):
            for x in range(limit):
                if not any(and_range((x, x), r) for r in ranges):
                    return x * 4_000_000 + row

    return None


print(part_2(sensor_beacon, 4_000_000))

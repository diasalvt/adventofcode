from functools import reduce


def load(filename: str) -> tuple[list[range], list[int]]:
    with open(filename) as f:
        ranges_str, data_str = f.read().split('\n\n')

    ranges = []
    for r in ranges_str.split():
        start, end = map(int, r.split('-'))
        ranges.append(range(start, end + 1))

    return (
        ranges,
        [int(v) for v in data_str.split()]
    )


ranges, data = load('input.txt')

print(
    len({
        v
        for v in data
        for r in ranges
        if v in r
    })
)


def before_after(r1: range, r2: range) -> tuple[list[range], range | None]:
    start_checks = (
        r1.start < r2.start,
        r2.start <= r1.start < r2.stop,
        r1.start >= r2.stop
    )
    end_checks = (
        r1.stop <= r2.start,
        r2.start < r1.stop <= r2.stop,
        r1.stop > r2.stop
    )
    match start_checks, end_checks:
        case _, (True, _, _):
            return ([r1, r2], None)
        case (_, _, True), _:
            return ([r2], r1)
        case (_, True, _), (_, True, _):
            return ([r2], None)
        case (_, True, _), (_, _, True):
            return ([range(r2.start, r2.stop)], range(r2.stop, r1.stop))
        case (True, _, _), (_, True, _):
            return ([range(r1.start, r2.stop)], None)
        case (True, _, _), (_, _, True):
            return ([range(r1.start, r2.stop)], range(r2.stop, r1.stop))
        case _:
            raise ValueError(f'Unexpected ranges {r1=}, {r2=}')


def add_range(l_sorted_ranges: list[range], r: range) -> list[range]:
    if len(l_sorted_ranges) == 0:
        return [r]

    first_range, *rest_ranges = l_sorted_ranges

    ranges, rest = before_after(r, first_range)
    if rest is None:
        return ranges + rest_ranges

    return ranges + add_range(rest_ranges, rest)


result = sum(map(len, reduce(add_range, ranges, [])))
print(result)

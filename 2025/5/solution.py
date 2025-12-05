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


def union(r1: range, r2: range) -> list[range]:
    
def add_range(r: range, l_sorted_ranges: list[range]) -> list[range]:
    start, end = r.start, r.stop - 1

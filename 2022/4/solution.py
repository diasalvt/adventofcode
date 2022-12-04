import re
from itertools import starmap

Range = tuple[int, int]


def parse_file(filename: str) -> list[tuple]:
    def str_to_range(s: str) -> Range:
        return tuple(map(int, re.findall(r'\d+', s)))

    with open(filename) as f:
        return [
            tuple(map(str_to_range, row.split(',')))
            for row in f.read().splitlines()
        ]


ranges = parse_file('input.txt')


def fully_contain(r1: Range, r2: Range):
    '''
        r1 fully contains r2
    '''
    r1a, r1b = r1
    r2a, r2b = r2
    return (r1a <= r2a) and (r2b <= r1b)


def overlap(r1: Range, r2: Range):
    '''
        r1 overlap with r2
    '''
    r1a, r1b = r1
    r2a, r2b = r2
    return (min(r2b, r1b) - max(r1a, r2a)) >= 0

print(
    sum(
        starmap(
            lambda r1, r2: fully_contain(r1, r2) or fully_contain(r2, r1),
            ranges
        )
    )
)


print(
    sum(
        starmap(
            lambda r1, r2: overlap(r2, r1),
            ranges
        )
    )
)
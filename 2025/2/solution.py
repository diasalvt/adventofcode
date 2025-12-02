from typing import Iterable
from math import log
from itertools import pairwise


def load(filename: str) -> list[tuple[int]]:
    with open(filename) as f:
        return [
            tuple(map(int, pair.split('-')))
            for pair in f.read().strip().split(',')
        ]


def is_valid_id(int):
    s = str(int)
    if (len(s) % 2) == 0:
        split = len(s)//2
        return s[:split] == s[split:]
    return False


input_data = load('input.txt')
result = sum(
    sum(i for i in range(lower, upper + 1) if is_valid_id(i))
    for lower, upper in input_data
)

print(result)


def power(start: int, end: int, base: int = 10) -> Iterable[int]:
    return [
        base ** exponent
        for exponent in range(
            int(log(start, base)) + 1, int(log(end, base)) + 1
        )
    ]


def split_range_by_len(r: range) -> list[range]:
    return [
        range(*p)
        for p in pairwise(
            [r.start] + power(r.start + 1, r.stop - 1) + [r.stop]
        )
    ]


def repeated_number_of_size(r: range, size: int = 1) -> list[int]:
    r_start, r_end = r.start, r.stop - 1

    length = len(str(r_start))
    if (length % size) != 0:
        return []

    min_digit, max_digit = int(str(r_start)[:size]), int(str(r_end)[:size])

    return [
        int(str(digits) * (length // size))
        for digits in range(min_digit, max_digit + 1)
        if int(str(digits) * (length // size)) in r
    ]


def repeated_number(r: range) -> set[int]:
    length = len(str(r.start))

    return {
        v
        for i in range(1, (length // 2) + 1)
        for v in repeated_number_of_size(r, i)
    }


result = sum(
    v
    for lower, upper in input_data
    for sub_r in split_range_by_len(range(lower, upper + 1))
    for v in repeated_number(sub_r)
)
print(result)

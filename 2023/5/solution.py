from typing import Self, Iterable, Optional, Generator
import re
from itertools import pairwise, chain, islice
from collections import defaultdict


Seeds = list[int]
Mapping = list[tuple[range, range]]


def extract_int(s: str) -> list[int]:
    return list(
        map(int, re.findall(r'\d+', s))
    )


def in_range(r1: range, r2: range) -> bool:
    if len(r1) == 0:
        return True
    if len(r2) == 0:
        return False
    return r1.start >= r2.start and r1.stop <= r2.stop


def range_intersect(
    r_a: range, r_b: range
) -> dict:

    def inter(r1: range, r2: range) -> Optional[range]:
        return range(
            max(r1.start, r2.start),
            min(r1.stop, r2.stop)
        ) or None

    result = defaultdict(list)
    r_a_and_r_b = inter(r_a, r_b)
    if not r_a_and_r_b:
        return {
            'a': [r_a],
            'b': [r_b],
            'inter': []
        }

    points = sorted([
        r_a.start,
        r_a.stop - 1,
        r_b.start,
        r_b.stop - 1
    ])

    for x, y in pairwise(points):
        r = range(x, y + 1)
        cutted_r = range(
            x + 1 if x in r_a_and_r_b else x,
            y if y in r_a_and_r_b else y + 1
        )
        match in_range(r, r_a), in_range(r, r_b):
            case True, False:
                result['a'] += [cutted_r]
            case False, True:
                result['b'] += [cutted_r]
            case True, True:
                result['inter'] += [r]
            case _:
                raise ValueError('Range intersect failure')

    return result


def range_shift(r: range, shift: int) -> range:
    return range(r.start + shift, r.stop + shift)


def transformed_range(
    r: range, r_source: range, r_dest: range
) -> tuple[list[range], list[range]]:
    intersection = range_intersect(r, r_source)
    shift = r_dest.start - r_source.start
    return (
        intersection['a'],
        [range_shift(inter, shift) for inter in intersection['inter']]
    )


# print(range_intersect(range(2, 5), range(4, 8)))
# print(range_intersect(range(2, 5), range(3, 4)))


class RangeMap:
    def __init__(self: Self, mapping: Mapping):
        self.mapping = mapping

    @classmethod
    def from_data(cls, data: list[tuple[int, int, int]]) -> Self:
        return cls(
            [
                (
                    range(source, source + length),
                    range(dest, dest + length),
                )
                for dest, source, length in data
            ]
        )

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls.from_data(
            [tuple(extract_int(line)) for line in s.split('\n') if len(line) > 0]
        )

    def __getitem__(self: Self, idx: int):
        for range_source, range_dest in self.mapping:
            if idx in range_source:
                return range_dest[range_source.index(idx)]
        return idx

    def transform_range(self: Self, r: range) -> Iterable[range]:
        current_input = [r]
        next_input = []
        output = []
        for range_source, range_dest in self.mapping:
            for r_in in current_input:
                not_inter, inter = transformed_range(r_in, range_source, range_dest)
                output.extend(inter)
                next_input.extend(not_inter)
            current_input = next_input
            next_input = []
        return output + current_input

    def __repr__(self):
        return str(self.mapping)


def test_rangemap():
    assert RangeMap.from_data([(50, 52, 2)])[52] == 50


def test_rangemap_from_str():
    assert RangeMap.from_str('50 52 2\n 40 43 4')[44] == 41


def load(filename: str) -> tuple[list[int], list[RangeMap]]:
    with open(filename) as f:
        seeds, *mappings = re.split(r'\n\n', f.read())
        seeds = extract_int(seeds)
        mappings = [
            RangeMap.from_str(mapping.split('\n', maxsplit=1)[1])
            for mapping in mappings
        ]
    return seeds, mappings


seeds, mappings = load('input.txt')
seeds_test, mappings_test = load('test.txt')


def transform_seed(seed: int, mappings: list[RangeMap]) -> int:
    current = seed
    for m in mappings:
        current = m[current]
    return current


def test_transform_seed():
    assert transform_seed(79, mappings_test) == 82


print(min(transform_seed(seed, mappings) for seed in seeds))


def batched(iterable: Iterable, n: int) -> Generator:
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


seeds = [range(start, start + length) for start, length in batched(seeds, 2)]
print(seeds)


def transform_range_seed(range_seed: range, mappings: list[RangeMap]) -> int:
    current_range = [range_seed]
    next_range = []

    for m in mappings:
        for r in current_range:
            next_range.extend(m.transform_range(r))
        current_range = next_range
        next_range = []

    return current_range


print(transform_range_seed(range(79, 79 + 14), mappings_test))
print(
    min(
        min(r.start for r in transform_range_seed(r, mappings))
        for r in seeds
    )
)

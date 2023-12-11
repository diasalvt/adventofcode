from typing import Self, Iterable, Optional
import re
from itertools import pairwise


Seeds = list[int]
Mapping = list[tuple[range, range]]


def extract_int(s: str) -> list[int]:
    return list(
        map(int, re.findall(r'\d+', s))
    )


def range_intersect_shift(
    r: range, source_r: range, dest_r: range
) -> Optional[range]:
    shift = dest_r.start - source_r.start
    return range(
        max(r.start, source_r.start) + shift,
        min(r.stop, source_r.stop) + shift
    ) or None


class RangeMap:
    def __init__(self: Self, mapping: Mapping):
        self.mapping = mapping

    @classmethod
    def from_data(cls, data: list[tuple[int, int, int]]) -> Self:
        print(data)
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
        return list(filter(
            lambda x: x is not None,
            (
                range_intersect_shift(r, range_source, range_dest)
                for range_source, range_dest in self.mapping
            )
        ))


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

seeds = (range(start, length) for start, length in pairwise(seeds))


def transform_range_seed(range_seed: range, mappings: list[RangeMap]) -> int:
    current_range = [range_seed]
    next_range = []

    for m in mappings:
        for r in current_range:
            print(r)
            next_range.extend(m.transform_range(r))
        current_range = next_range
        next_range = []

    return current_range


print(transform_range_seed(range(79, 79 + 14), mappings_test))

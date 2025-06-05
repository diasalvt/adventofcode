from collections import Counter, defaultdict
from itertools import tee, islice
from typing import Iterator, Iterable

Plant = str | int
Garden = dict[complex, Plant]


def load(filename: str) -> Garden:
    garden: Garden = {}
    with open(filename) as f:
        for j, row in enumerate(f.read().splitlines()):
            for i, c in enumerate(row):
                garden[i + j * 1j] = c
    return garden


test = load('test.txt')
garden = load('input.txt')


def neighbours(
    garden: Garden, pos: complex
) -> tuple[complex]:

    return tuple(
        pos + i + j * 1j
        for i, j in {(-1, 0), (0, -1), (0, 1), (1, 0)}
        if (pos + (i + j * 1j)) in garden
    )

# def contiguous(garden: Garden, pos: complex) -> list[complex]:
#     plant = garden[pos]
#     seen = set()

#     def _contiguous_plant(
#         garden: Garden, pos: complex, seen: set[complex] = seen
#     ) -> list[complex]:
#         seen |= {pos}
#         return [pos] + list(chain.from_iterable(
#             _contiguous_plant(garden, n)
#             for n in neighbours(garden, pos)
#             if (garden[n] == plant) and (n not in seen)
#         ))

#     return _contiguous_plant(garden, pos, seen=seen)


def contiguous(garden: Garden, pos: complex) -> list[complex]:
    plant = garden[pos]
    to_explore = [pos]
    seen = set()

    while to_explore:
        current = to_explore.pop()
        if current not in seen:
            for n in neighbours(garden, current):
                if garden[n] == plant:
                    to_explore.append(n)
            seen |= {current}
    return list(seen)


def replace_letter_by_number(garden: Garden) -> Garden:
    new_garden: Garden = {}
    i = 0
    for pos, plant in garden.items():
        if pos not in new_garden:
            for c in contiguous(garden, pos):
                new_garden[c] = i
            i += 1
    return new_garden


def areas(garden: Garden) -> Counter:
    return Counter(garden.values())


def perimeter(garden: Garden) -> defaultdict[str, int]:
    d = defaultdict(int)
    for pos, plant in garden.items():
        border = (
            4 -
            sum(1 for n in neighbours(garden, pos) if garden[n] == plant)
        )
        d[plant] += border
    return d


def part1(garden: Garden) -> int:
    new_garden = replace_letter_by_number(garden)
    garden_areas = areas(new_garden)
    garden_perimeter = perimeter(new_garden)

    return sum(
        count * garden_perimeter[plant]
        for plant, count in garden_areas.items()
    )


print(part1(garden))


def nwise(it: Iterable, n: int) -> Iterator:
    return zip(*(islice(it, s, None) for s, it in enumerate(tee(it, n))))


def count_corners_pos(garden: Garden, pos: complex) -> int:
    def pos_around(
        garden: Garden, pos: complex
    ) -> tuple[complex]:

        return list(
            nwise((
                pos + i + j * 1j
                for i, j in [
                    (-1, 0), (-1, -1), (0, -1), (1, -1),
                    (1, 0), (1, 1), (0, 1),
                    (-1, 1), (-1, 0)
                ]
            ), 3)
        )

    outer_corners = sum(
        garden[pos] not in {garden.get(n_1, -1), garden.get(n_3, -1)}
        for n_1, n_2, n_3 in pos_around(garden, pos)
        if abs(n_2 - pos) > 1
    )
    interior_corners = sum(
        (
            (garden.get(n_1, -1) == garden.get(n_3, -1) == garden[pos]) and
            (garden.get(n_2, -1) != garden[pos])
        )
        for n_1, n_2, n_3 in pos_around(garden, pos)
        if abs(n_2 - pos) > 1
    )

    return outer_corners + interior_corners


def part2(garden: Garden) -> int:
    new_garden = replace_letter_by_number(garden)
    garden_areas = areas(new_garden)

    garden_modified_perimeter = defaultdict(int)
    for pos, plant in new_garden.items():
        garden_modified_perimeter[plant] += count_corners_pos(new_garden, pos)

    return sum(
        count * garden_modified_perimeter[plant]
        for plant, count in garden_areas.items()
    )


print(part2(garden))

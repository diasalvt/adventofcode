import re
from collections import defaultdict
from math import prod


def load(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().splitlines()


schematic = load("input.txt")
schematic_test = load("test.txt")


def pad(schematic: list[str]) -> list[str]:
    width = len(schematic[0]) + 2
    return (
        ['.' * width] +
        [
            '.' + line + '.'
            for line in schematic
        ] +
        ['.' * width]
    )


padded_schematic = pad(schematic)


def neighborhood(
    start: int,
    end: int,
    line_number: int,
    schematic: list[str]
) -> str:
    return (
        schematic[line_number - 1][start - 1:end + 2] +
        schematic[line_number][start - 1] + schematic[line_number][end + 1] +
        schematic[line_number + 1][start - 1:end + 2]
    )


def sum_numbers_line(i: int, schematic: list[str]) -> list[int]:
    res = []
    for match in re.finditer(r'\d+', schematic[i]):
        start, end = match.span()
        end = end - 1
        if re.findall(r'[^\d\.]', neighborhood(start, end, i, schematic)):
            res.append(
                int(match.group(0))
            )
    return sum(res)


print(
    sum(
        sum_numbers_line(i, padded_schematic)
        for i in range(1, len(schematic) + 1)
    )
)


def neighborhood_2(
    start: int,
    end: int,
    line_number: int,
    schematic: list[str]
) -> tuple[str, str, str]:
    return (
        schematic[line_number - 1][start - 1:end + 2],
        (
            schematic[line_number][start - 1] +
            ('.' * (end - start + 1)) +
            schematic[line_number][end + 1]
        ),
        schematic[line_number + 1][start - 1:end + 2]
    )


Pos = tuple[int, int]


def asterix_numbers_line(
    i: int, schematic: list[str], observed: defaultdict[list]
) -> defaultdict[Pos, list[int]]:
    for match in re.finditer(r'\d+', schematic[i]):
        start, end = match.span()
        end = end - 1
        for j, line in enumerate(neighborhood_2(start, end, i, schematic), -1):
            for asterix_match in re.finditer(r'\*', line):
                pos = (i + j, start + asterix_match.start() - 1)
                observed[pos].append(int(match.group(0)))
    return observed


def compute_gears(schematic: list[str]) -> int:
    asterix_neighbours = defaultdict(list)
    for i in range(1, len(pad(schematic))):
        asterix_neighbours = asterix_numbers_line(i, pad(schematic), asterix_neighbours)

    return sum(prod(numbers) for asterix_pos, numbers in asterix_neighbours.items() if len(numbers) > 1)


def test_compute_gears():
    compute_gears(pad(schematic_test)) == 467835


print(
    compute_gears(padded_schematic)
)

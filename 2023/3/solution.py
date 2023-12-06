import re


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
        schematic[line_number - 1][start - 1:end + 1] +
        schematic[line_number][start - 1] + schematic[line_number][end] +
        schematic[line_number + 1][start - 1:end + 1]
    )


def sum_numbers_line(i: int, schematic: list[str]) -> list[int]:
    res = []
    for match in re.finditer(r'\d+', schematic[i]):
        start, end = match.span()
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

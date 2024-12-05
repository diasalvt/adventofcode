import re


def parse(filename: str) -> list[tuple[int, int]]:
    with open(filename) as f:
        return [
            tuple(map(int, pair))
            for pair in re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', f.read())
        ]


puzzle = parse('input.txt')
print(puzzle)

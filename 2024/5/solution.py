from typing import TypeAlias


Requirements: TypeAlias = list[tuple[int, int]]
Codes: TypeAlias = list[list[int]]


def load(filename: str) -> tuple[Requirements, Codes]:
    with open(filename) as f:
        reqs, codes = f.read().split('\n\n')
        reqs = [
            (int(pair_str[:2]), int(pair_str[3:])) for pair_str in reqs.split()
        ]
        codes = [
            list(map(int, code_str.split(','))) for code_str in codes.split()
        ]

        return reqs, codes


reqs, codes = load('input.txt')




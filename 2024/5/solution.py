from typing import TypeAlias


Requirements: TypeAlias = list[tuple[int, int]]
Code: TypeAlias = list[int]


def load(filename: str) -> tuple[Requirements, list[Code]]:
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


def code_is_valid(reqs: Requirements, code: Code) -> bool:
    for before, after in reqs:
        try:
            if code.index(before) >= code.index(after):
                return False
        except ValueError:
            pass
    return True


def solve(reqs: Requirements, codes: list[Code]) -> int:
    res = 0
    for code in codes:
        if code_is_valid(reqs, code):
            res += code[len(code) // 2]
    return res


print(solve(reqs, codes))


def get_middle_numbers(reqs: Requirements, code: Code) -> int:
    for c in code:
        number_before = sum(1 for (a, b) in reqs if (b == c) and (a in code))
        number_after = sum(1 for (a, b) in reqs if (a == c) and (b in code))

        if number_before == number_after:
            return c


def solve_part2(reqs: Requirements, codes: list[Code]) -> int:
    res = 0
    for code in codes:
        if not code_is_valid(reqs, code):
            res += get_middle_numbers(reqs, code)
    return res


print(solve_part2(reqs, codes))

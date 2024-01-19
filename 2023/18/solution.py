from itertools import accumulate, pairwise
from operator import add

Inst = tuple[complex, int, str]


def load(filename: str) -> list[Inst]:
    def str_to_inst(s: str) -> Inst:
        dirs = {
            'D': -1j, 'U': 1j, 'L': -1, 'R': 1
        }
        dir, count, color = s.split()
        return (dirs[dir], int(count), color[2:-1])

    return [
        str_to_inst(row)
        for row in open(filename).read().splitlines()
    ]


test = load('test.txt')
instructions = load('input.txt')


def instructions_to_points(instructions: list[Inst]) -> list[complex]:
    shifts = (count * dir for dir, count, _ in instructions)
    return list(accumulate(shifts, add, initial=0))


def shoelace(points: list[complex]) -> int:
    return (
        sum(abs(p2 - p1) for p1, p2 in pairwise(points)) +
        abs(sum(
            (p1.imag + p2.imag) * (p1.real - p2.real)
            for p1, p2 in pairwise(points)
        ))
    ) / 2 + 1


print(shoelace(instructions_to_points(instructions)))


def extract_instructions(instructions: list[Inst]) -> list[Inst]:
    return [
        (
            [1, -1j, -1, 1j][int(color[-1])],
            int(color[:-1], 16),
            color
        )
        for _, _, color in instructions
    ]


print(
    shoelace(instructions_to_points(extract_instructions(instructions)))
)

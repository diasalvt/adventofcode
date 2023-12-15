from typing import Generator


def parse(line: str) -> tuple[str, list[int]]:
    springs, conditions = line.split()
    conditions = [int(v) for v in conditions.split(',')]
    return springs, conditions


def load(filename: str) -> list[tuple[str, list[int]]]:
    return [parse(line) for line in open(filename)]


game = load('input.txt')
game_test = load('test.txt')


def generate_springs(conditions: list[int], length: int) -> Generator:
    nb_mandatory_dots = len(conditions) - 1
    nb_additional_dots = length - (sum(conditions) - nb_mandatory_dots)

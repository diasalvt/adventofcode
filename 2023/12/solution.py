from typing import Generator, Callable
from functools import cache
from tqdm import tqdm


def parse(line: str) -> tuple[str, list[int]]:
    springs, conditions = line.split()
    conditions = [int(v) for v in conditions.split(',')]
    return springs, conditions


def load(filename: str) -> list[tuple[str, list[int]]]:
    return [parse(line) for line in open(filename)]


game = load('input.txt')
game_test = load('test.txt')


def is_valid(pattern: str, springs: str):
    for char_pattern, char_springs in zip(pattern, springs):
        if char_pattern != '?':
            if char_pattern != char_springs:
                return False
    return True


def dots_sharps_gen(pattern: str, conditions: tuple[int], min_val: int = 0) -> Generator:
    if not conditions:
        if is_valid(pattern, rest := '.' * len(pattern)):
            yield rest
    else:
        for value in range(min_val, len(pattern) - (len(conditions) + sum(conditions)) + 2):
            curr = '.' * value + '#' * conditions[0]
            pattern_to_match, rest_pattern = pattern[:len(curr)], pattern[len(curr):]
            for rest in dots_sharps(
                rest_pattern,
                conditions[1:],
                min_val=1
            ):
                if is_valid(pattern_to_match, curr):
                    yield curr + rest


@cache
def dots_sharps(pattern: str, conditions: tuple[int], min_val: int = 0) -> list:
    if not conditions:
        if is_valid(pattern, rest := '.' * len(pattern)):
            return [rest]
        return []
    else:
        res = []
        for value in range(min_val, len(pattern) - (len(conditions) + sum(conditions)) + 2):
            curr = '.' * value + '#' * conditions[0]
            pattern_to_match, rest_pattern = pattern[:len(curr)], pattern[len(curr):]
            if is_valid(pattern_to_match, curr):
                res += [
                    curr + rest
                    for rest in dots_sharps(
                        rest_pattern,
                        conditions[1:],
                        min_val=1
                    )
                ]
        return res

print(
    sum(
        len(list(dots_sharps_gen(pattern, tuple(conditions))))
        for pattern, conditions in game
    )
)


print(
    sum(
        len(dots_sharps(pattern, tuple(conditions)))
        for pattern, conditions in game
    )
)


def augment(f: Callable) -> Callable:
    def augmented_f(pattern, conditions, *args, **kwargs):
        return f('?'.join([pattern]*5), tuple(conditions)*5, *args, *kwargs)
    return augmented_f


print(
    sum(
        sum(1 for x in augment(dots_sharps)(pattern, conditions))
        for pattern, conditions in tqdm(game_test)
    )
)

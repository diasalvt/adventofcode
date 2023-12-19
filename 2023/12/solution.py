from typing import Generator, Callable, Sequence, Any
from functools import cache


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


def augment(f: Callable, repeat: int = 1) -> Callable:
    def augmented_f(pattern, conditions, *args, **kwargs):
        return f(
            '?'.join([pattern]*repeat),
            tuple(conditions)*repeat, *args, *kwargs
        )
    return augmented_f


def split_pivot(seq: Sequence, i: int, l: int = 1) -> tuple[Sequence, Any, Sequence]:
    return seq[:i], seq[i: i + l], seq[i + l:]

def itersplit(seq: Sequence, l: int = 1) -> Generator:
    for i in range(len(seq)):
        yield split_pivot(seq, i, l)


@cache
def count_dots_sharps(pattern: str, conditions: tuple) -> int:
    if not pattern:
        return 1 if not conditions else 0
    if not conditions:
        return 1 if '#' not in pattern else 0
    if len(pattern) < (sum(conditions) + len(conditions) - 1):
        return 0

    pivot_idx = len(pattern) // 2
    pattern_before, pivot, pattern_after = split_pivot(pattern, pivot_idx)
    match pivot:
        case '.':
            return sum(
                (
                    count_dots_sharps(pattern_before, conditions[:i]) *
                    count_dots_sharps(pattern_after, conditions[i:])
                )
                for i in range(len(conditions) + 1)
            )
        case '#':
            res = 0
            pattern = '.' + pattern_before + 'P' + pattern_after + '.' # Padding pattern
            for cond_before, (cond,), cond_after in itersplit(conditions):
                for p_before, to_match, p_after in itersplit(pattern, cond + 2):
                    if 'P' in to_match:
                        to_match = to_match.replace('P', '#')
                        if is_valid(to_match, '.' + '#' * cond + '.'):
                            res += (
                                count_dots_sharps(p_before, cond_before) *
                                count_dots_sharps(p_after, cond_after)
                            )
            return res
        case '?':
            pattern_dot = pattern_before + '.' + pattern_after
            pattern_sharp = pattern_before + '#' + pattern_after
            return (
                count_dots_sharps(pattern_dot, conditions) +
                count_dots_sharps(pattern_sharp, conditions)
            )


print(
    sum(
        augment(count_dots_sharps, 5)(pattern, tuple(conditions))
        for pattern, conditions in game
    )
)

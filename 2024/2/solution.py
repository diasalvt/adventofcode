from typing import TypeAlias, Iterable, Generator, Any
from itertools import pairwise, chain, islice, tee, starmap

Report: TypeAlias = list[int]


def reports(filename: str) -> Iterable[Report]:
    with open(filename) as f:
        return list(map(
            lambda x: list(map(int, x.split())),
            f.read().splitlines()
        ))


def is_valid(rep: Report) -> bool:
    diffs = [a - b for a, b in pairwise(rep)]
    increasing = all(map(lambda x: x > 0, diffs))
    decreasing = all(map(lambda x: x < 0, diffs))
    return (
        (increasing or decreasing) and
        (max(map(abs, diffs)) <= 3)
    )


def except_one(it: Iterable) -> Generator[Any, None, None]:
    for i, _ in enumerate(it):
        yield chain(islice(it, 0, i), islice(it, i+1, None))


reps = reports('input.txt')
print(sum(is_valid(r) for r in reps))
print(
    sum(
        is_valid(r) or any(is_valid(sub_r)for sub_r in except_one(r))
        for r in reps
    )
)


def sliding_window(it: Iterable, n: int) -> Generator:
    yield from zip(
        *[
            islice(it_i, i, None)
            for i, it_i in enumerate(tee(it, n))
        ]
    )


def is_valid_except_one(rep: Report) -> bool:
    def _is_valid(x, y):
        if (x is None) or (y is None):
            return True
        return (1 <= (y - x) <= 3)

    def _increasing(rep: Report, can_skip: int = 1) -> bool:
        rep_with_sentinels = list(chain([None], rep, [None]))
        window = sliding_window(rep_with_sentinels, 4)
        is_valid_interval = sliding_window(
            starmap(_is_valid, pairwise(rep_with_sentinels)),
            3
        )

        for w, is_valid_increase in zip(window, is_valid_interval):
            a1, a2, a3, a4 = w

            match is_valid_increase:
                case True, False, False:
                    if not _is_valid(a2, a4):
                        return False
                    can_skip -= 1
                case True, False, True:
                    if not (_is_valid(a1, a3) or _is_valid(a2, a4)):
                        return False
                    can_skip -= 1
                case False, False, False:
                    return False
            if can_skip < 0:
                return False
        return True

    return (_increasing(rep) or _increasing(rep[::-1]))


print(sum(is_valid_except_one(r) for r in reps))

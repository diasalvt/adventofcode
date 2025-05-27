from itertools import chain
from typing import Callable
from functools import cache


def load_stones(filename: str) -> tuple[int]:
    with open(filename) as f:
        return tuple(map(int, f.read().split()))


stones = load_stones('input.txt')
print(stones)


def process(stone: int) -> tuple[int]:
    if stone == 0:
        return (1,)
    elif ((l := len(str(stone))) % 2) == 0:
        return (int(str(stone)[:l//2]), int(str(stone)[l//2:]))
    else:
        return (stone * 2024,)


def blink(stones: tuple[int]) -> tuple[int]:
    return tuple(
        chain.from_iterable(
            process(stone)
            for stone in stones
        )
    )


def repeat(func: Callable, n: int = 1) -> Callable:
    if n == 1:
        return func
    return lambda x: func(repeat(func, n-1)(x))


print(len(repeat(blink, 25)(stones)))


@cache
def count_stones(stone: int, steps: int) -> int:
    if steps == 0:
        return 1

    return sum(
        count_stones(s, steps-1) for s in process(stone)
    )


print(sum(count_stones(s, 75) for s in stones))

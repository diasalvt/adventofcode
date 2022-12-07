from typing import *
from itertools import tee


def parse_file(filename: str) -> str:
    with open(filename) as f:
        cmd = f.read()

    return cmd


cmd = parse_file('input.txt')


def nwise(it: Iterable, size: int = 2) -> Generator:
    iterators = list(tee(it, size))
    for i in range(1, size):
        for j in range(i, size):
            next(iterators[j])

    return zip(*iterators)


def idx_first_block(s: str, n: int = 4) -> int:
    return next(
        i + n
        for i, window in enumerate(nwise(s, n))
        if len(set(window)) == n
    )


def test_idx_first():
    assert idx_first_block('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
    assert idx_first_block('nppdvjthqldpwncqszvftbrmjlhg') == 6
    assert idx_first_block('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
    assert idx_first_block('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11


print(idx_first_block(cmd))


def test_idx_first_part2():
    assert idx_first_block('mjqjpqmgbljsphdztnvjfqwrcgsmlb', n=14) == 19
    assert idx_first_block('bvwbjplbgvbhsrlpgdmjqwftvncz', n=14) == 23
    assert idx_first_block('nppdvjthqldpwncqszvftbrmjlhg', n=14) == 23
    assert idx_first_block('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', n=14) == 29
    assert idx_first_block('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', n=14) == 26


print(idx_first_block(cmd, n=14))

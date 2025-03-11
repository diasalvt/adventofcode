from itertools import chain, islice, count, accumulate
from typing import Iterable, Iterator
import re


def load(filename: str) -> tuple[list[int], list[int]]:
    with open(filename) as f:
        disk = list(map(int, f.read().strip()))
    return disk[::2], disk[1::2]


disk = load('input.txt')


def interleave(*iterables: Iterable) -> Iterator:
    iterators = [it.__iter__() for it in iterables]
    for _ in count():
        for it in iterators:
            try:
                yield next(it)
            except StopIteration:
                return


def checksum(files: list[int], free_space: list[int]) -> int:
    files_ids_expanded = [[id] * count for id, count in enumerate(files)]
    files_ids_expanded_flat = list(chain.from_iterable(files_ids_expanded))

    reversed_files_ids_expanded = reversed(files_ids_expanded_flat)

    moved_files = map(
        lambda x: list(islice(reversed_files_ids_expanded, x)), free_space
    )
    return islice(
        chain.from_iterable(interleave(files_ids_expanded, moved_files)),
        len(files_ids_expanded_flat)
    )


print(
    sum(
        i * val
        for i, val in enumerate(checksum(*disk))
    )
)


def disk_str(flat_disk: list[int]) -> str:
    return ''.join(
        size * (' ' if i % 2 else 'x') for i, size in enumerate(flat_disk)
    )


def find_spot(s: str, file_pos, file_size) -> int:
    match = re.search(' ' * file_size, s)
    if match and (match.start() < file_pos):
        start = match.start()
        return (
            (
                s[:start] +
                'x' * file_size +
                s[start + file_size:file_pos] +
                ' ' * file_size +
                s[file_pos + file_size:]
            ),
            start
        )
    else:
        return s, file_pos


def play(disk: tuple[list[int], list[int]]) -> int:
    flat_disk = list(interleave(disk[0], disk[1]))
    positions = list(accumulate([0] + flat_disk))
    files_pos = positions[::2]
    files_size = disk[0]
    files = list(enumerate(zip(files_pos, files_size)))

    mem = disk_str(flat_disk)
    score = 0
    for id, (pos, size) in reversed(files):
        mem, pos = find_spot(mem, pos, size)
        score += sum(p * id for p in range(pos, pos + size))

    return score


print(play(disk))

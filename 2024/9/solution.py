from itertools import chain, islice, count, starmap, repeat
from typing import Iterable, Iterator, Optional


def load(filename: str) -> tuple[list[int], list[int]]:
    with open(filename) as f:
        disk = list(map(int, f.read().strip()))
    return disk[::2], disk[1::2]


disk = load('test2.txt')


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

mem = (list(enumerate(disk[0])), disk[1] + [0])

FileSizes = list[tuple[int, int]]
FreeSpaces = list[int]  # Indicate the number of free spaces also at the end
Memory = tuple[FileSizes, FreeSpaces]


def combine_mems(*mems: Memory) -> Memory:
    return tuple(
        map(lambda x: list(chain.from_iterable(x)), zip(*mems))
    )


def mem_pop(mem: Memory) -> tuple[Memory, tuple[int, int]]:
    file_sizes, free_spaces = mem
    return (
        file_sizes[:-1],
        free_spaces[:-2] + [free_spaces[-2] + free_spaces[-1] + file_sizes[-1][1]]
    ), file_sizes[-1]


def mem_append(mem: Memory, file_size) -> Optional[Memory]:
    file_sizes, free_spaces = mem
    file_id, size = file_size
    if free_spaces[-1] >= size:
        return (
            file_sizes + [file_size],
            free_spaces[:-1] + [0, free_spaces[-1] - size]
        )
    else:
        return None


def sub_mem(mem: Memory, start: int, stop: int) -> Memory:
    file_sizes, free_spaces = mem
    return (
        file_sizes[start:stop],
        free_spaces[start:stop]
    )


def sub_mems(mem: Memory) -> Iterator[tuple[Memory]]:
    for i in range(1, len(mem[0])):
        yield sub_mem(mem, 0, i), sub_mem(mem, i, None)


def mem_insert_left_most(mem: Memory, file_size) -> Optional[Memory]:
    for mem_before, mem_after in sub_mems(mem):
        if new_mem := mem_append(mem_before, file_size):
            return combine_mems(new_mem, mem_after)
    return None


def move(mem: Memory, file_id) -> Optional[Memory]:
    file_id_pos = [i for i, (id, _) in enumerate(mem[0]) if id == file_id][0]
    mem_before, mem_after = (
        sub_mem(mem, 0, file_id_pos + 1),
        sub_mem(mem, file_id_pos + 1, None)
    )
    mem_before, file_size = mem_pop(mem_before)
    if new_mem := mem_insert_left_most(mem_before, file_size):
        return combine_mems(new_mem, mem_after)
    else:
        return mem


def score_mem(mem: Memory) -> int:
    file_sizes, free_spaces = mem
    flatten_mem = chain.from_iterable(
        interleave(
            starmap(repeat, file_sizes), map(lambda x: ['.'] * x, free_spaces)
        )
    )
    return sum(
        i * v
        for i, v in enumerate(flatten_mem)
        if v != '.'
    )


def play(mem: Memory) -> int:
    for i in reversed(range(1, len(mem[0]))):
        mem = move(mem, i)
    return mem


print(score_mem(play(mem)))

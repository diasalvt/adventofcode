from typing import Generator, Iterable
from itertools import islice


def load(filename: str) -> list[tuple[int]]:
    with open(filename) as f:
        definition_str = f.read().splitlines()
    return [
        tuple(int(elem) for elem in definition.split())
        for definition in definition_str
    ]


definitions = load('input.txt')


def count_triangles(definitions: list[tuple[int]]) -> int:
    def is_triangle(definition: tuple[int]) -> bool:
        total_length = sum(definition)
        return all(total_length > (2*side) for side in definition)

    return sum(map(is_triangle, definitions))


def batched(it: Iterable, *, n=2) -> Generator:
    it = iter(it)
    while batch := tuple(islice(it, n)):
        yield batch


def transform_definitions(definitions: list[tuple[int]]) -> Generator:
    for defs in batched(definitions, n=3):
        for new_def in zip(*defs):
            yield new_def


print(count_triangles(definitions))
print(count_triangles(transform_definitions(definitions)))

import re
import pytest


def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().splitlines()


test = get_data('test.txt')
print(test)

special_characters = [
    r'\\\\',
    r'\\"',
    r'\\x..',
    r'.'
]


def character_count(line: str) -> int:
    line = line[1:-1]
    i = 0
    count = 0
    while i < len(line):
        for special_character in special_characters:
            if m := re.match(special_character, line[i:]):
                i += (m.end() - m.start())
                count += 1
                break
    return count


def solution(data: list[str]) -> int:
    return sum(len(l) - character_count(l) for l in data)


@pytest.mark.parametrize(
    'line, count',
    [
        (r'""', 0),
        (r'"abc"', 3),
        (r'"aaa\"aaa"', 7),
        (r'"\x27"', 1)
    ]
)
def test_character_count(line: str, count: int):
    assert character_count(line) == count


def test_solution():
    assert solution(test) == 12


print(solution(get_data('input.txt')))


def solution_part_2(data: list[str]) -> int:
    return sum(2 + sum(l.count(c) for c in r'\"') for l in data)


def test_solution_part_2():
    assert solution_part_2(test) == 19


print(solution_part_2(get_data('input.txt')))

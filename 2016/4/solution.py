import re
from collections import Counter

Message = tuple[str, int, str]


def load(filename: str) -> list[Message]:
    with open(filename) as f:
        lines = f.read().splitlines()

    return [
        re.fullmatch(
            r'(?P<characters>[\w\-]+)-(?P<id>\d+)\[(?P<checksum>\w+)\]',
            line
        ).groups()
        for line in lines
    ]


def compute_checksum(s: str) -> str:
    s_no_dash = [c for c in s if c != '-']
    return [
        c
        for c, count in sorted(
            Counter(s_no_dash).most_common(5), key=lambda x: (-x[1], x[0])
        )
    ]


print(compute_checksum('aaaaa-bbb-z-y-x'))


def validate(characters: str, checksum: str) -> bool:
    return compute_checksum(characters) == checksum


messages = load('input.txt')

# for characters, _, checksum in messages:
#     print(f'{characters}, {checksum}: {validate(characters, checksum)}')


print(
    sum(validate(characters, checksum) for characters, _, checksum in messages)
)

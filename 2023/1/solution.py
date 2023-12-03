import regex as re


def load(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().splitlines()


first_num = re.compile(r'^[^\d]*(\d)')
last_num = re.compile(r'(\d)[^\d]*$')


def extract(s: str) -> int:
    search = lambda x, y: re.search(x, y).group(1)
    return int(search(first_num, s) + search(last_num, s))


print(
    inp := load('input.txt')
)

print(
    sum(map(extract, inp))
)

numbers_str = [
    'one', 'two', 'three', 'four', 'five',
    'six', 'seven', 'eight', 'nine'
]


numeric = re.compile(f'{"|".join(numbers_str)}|[1-9]')
print(numeric)


def str_to_intstr(s: str) -> str:
    try:
        return str(numbers_str.index(s) + 1)
    except ValueError:
        return s


def extract_2(s: str) -> int:
    matches = list(map(str_to_intstr, re.findall(numeric, s, overlapped=True)))
    if len(matches) < 1:
        raise ValueError(f'{matches=} is not valid')
    return int(matches[0] + matches[-1])


def test_extract_2():
    test = load('test.txt')
    assert sum(map(extract_2, test)) == 281


print(
    sum(map(extract_2, inp))
)

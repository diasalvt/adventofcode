from itertools import count

Snafu = str

_snafu_base = 5


def parse_file(filename: str) -> list[Snafu]:
    with open(filename) as f:
        return f.read().splitlines()


test = parse_file('test.txt')
print(test)


_conv_snafu = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}


_conv_snafu_inv = {
    2: '2',
    1: '1',
    0: '0',
    -1: '-',
    -2: '='
}


def snafu_to_int(snafu: Snafu) -> int:
    result = 0
    for char in snafu:
        result *= _snafu_base
        result += _conv_snafu[char]
    return result


print(snafu_to_int('1=-0-2'))
print(snafu_to_int('2000000'))
print(snafu_to_int('2======'))


def int_to_snafu(val: int) -> Snafu:

    def upper_lower_bound(size: int) -> tuple[int, int]:
        bound = (5**size - 1) // 2
        return (-int(bound), int(bound))

    size_snafu = next(filter(
        lambda x: x[0],
        ((val in range(*upper_lower_bound(i)), i) for i in count(1))
    ))[1]

    def char(val: int, size: int) -> int:
        if val in _conv_snafu_inv:
            return _conv_snafu_inv[val]

        i = size - 1
        if val >= 0:
            q = val // (_snafu_base**i)
            if val - q * _snafu_base ** i not in range(*upper_lower_bound(i)):
                q += 1
            return str(q) + char(val - q * _snafu_base ** i, size - 1)
        else:
            q = (-val) // (_snafu_base**i)
            if val + q * _snafu_base ** i not in range(*upper_lower_bound(i)):
                q += 1
            return _conv_snafu_inv[-q] + char(val + q * _snafu_base ** i, size - 1)
    return char(val, size_snafu)


print(int_to_snafu(12345))
print(int_to_snafu(314159265))


def part_1(filename: str) -> Snafu:
    snafus = parse_file(filename)
    return int_to_snafu(sum(snafu_to_int(val) for val in snafus))


print(part_1('test.txt'))
print(part_1('input.txt'))

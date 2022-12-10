from itertools import repeat, chain


def parse_file(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().splitlines()


cmds = parse_file('input.txt')
cmds_test = parse_file('test.txt')


def cycles(cmds: list[str]) -> list[int]:
    x = [1]

    for cmd in cmds:
        op, *param = cmd.split()
        x += [x[-1]]
        if op == 'addx':
            x += [x[-1] + int(param[0])]

    return x


def part_1(cmds: list[str]) -> int:
    val_x = cycles(cmds)

    return sum(x * y for x, y in zip(val_x[19:220:40], range(20, 221, 40)))


def test_part_1():
    assert part_1(parse_file('test.txt')) == 13140


print(part_1(cmds))


def part_2(cmds: list[str]) -> int:
    val_x = cycles(cmds)
    print(val_x)
    return [
        abs(crt_pos - x) < 2
        for crt_pos, x in zip(chain(*repeat(range(40), 6)), val_x)
    ]


def print_crt(pixel: list[bool]) -> None:
    for i in range(6):
        print(''.join(['#' if p else '.' for p in pixel[40*i:40*(i+1)]]))


print_crt(part_2(cmds))

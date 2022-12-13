from typing import TypeAlias, Optional
from itertools import zip_longest, chain
from functools import cmp_to_key
from math import prod

Packet: TypeAlias = list


def parse_file(filename: str) -> list[tuple[Packet, Packet]]:
    with open(filename) as f:
        return [
            (eval(p1), eval(p2))
            for p1, p2 in map(lambda x: x.splitlines(), f.read().split('\n\n'))
        ]


test = parse_file('test.txt')


def compare(left: Packet, right: Packet) -> Optional[bool]:
    match (left, right):
        case (_, None):
            return False
        case (None, _):
            return True
        case (int(a), int(b)):
            if a == b:
                return None
            else:
                return a < b
        case (list(l_left), list(l_right)):
            for a, b in zip_longest(l_left, l_right):
                if (res := compare(a, b)) is not None:
                    return res
        case (int(a), list(l_right)):
            return compare([a], l_right)
        case (list(l_left), int(b)):
            return compare(l_left, [b])


def final_compare(left: Packet, right: Packet) -> bool:
    res = compare(left, right)
    return res if res is not None else True


def test_compare():
    test = parse_file('test.txt')
    assert final_compare(*test[0]) == True
    assert final_compare(*test[1]) == True
    assert final_compare(*test[2]) == False
    assert final_compare(*test[3]) == True
    assert final_compare(*test[4]) == False
    assert final_compare(*test[5]) == True
    assert final_compare(*test[6]) == False
    assert final_compare(*test[7]) == False


def part_1(packets: list[tuple[Packet, Packet]]) -> int:
    return sum(i + 1 for i, (left, right) in enumerate(packets) if final_compare(left, right))


def test_part_1():
    test = parse_file('test.txt')
    assert part_1(test) == 13


print(part_1(parse_file('input.txt')))


def part_2(packets: list[tuple[Packet, Packet]]) -> int:
    all_packets = list(chain(*packets, [[[2]], [[6]]]))

    def cmp(a, b):
        match compare(a, b):
            case True:
                return 1
            case False:
                return -1
            case _:
                return 0
    sorted_packets = sorted(all_packets, key=cmp_to_key(cmp), reverse=True)
    return prod(i + 1 for i, p in enumerate(sorted_packets) if p in [[[2]], [[6]]])


print(part_2(parse_file('input.txt')))

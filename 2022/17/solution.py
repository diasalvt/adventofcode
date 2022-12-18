from dataclasses import dataclass, field
from typing import TypeAlias, Iterator
from itertools import cycle, islice

Cmd: TypeAlias = str
Pos: TypeAlias = complex
Fig: TypeAlias = set[Pos]


def parse_file(filename: str) -> list[Cmd]:
    with open(filename) as f:
        return list(f.readline().strip('\n'))


cmds_test = parse_file('test.txt')


figures = [
    {0, 1j, 2j, 3j},  # horizontal line
    {1j, 1, 1 + 1j, 1 + 2j, 2 + 1j},  # cross
    {0, 1j, 2j, 1 + 2j, 2 + 2j},  # _|
    {0, 1, 2, 3},  # vertical line
    {0, 1j, 1, 1 + 1j},  # square
]

cmd_move = {
    '>': 1j,
    '<': -1j
}


@dataclass
class Chamber:
    rocks: set
    bottom: complex = field(default=0)

    def positions_are_valid(self, pos: set[Pos]) -> bool:
        return all(
            (0 <= p.imag <= 6) and (p.real >= 0) and (p not in self.rocks)
            for p in pos
        )

    def _move(self, figure: Fig, cmd: Cmd) -> tuple[Fig, bool]:
        """
            return: Figure after move and boolean if figure is currently moving
        """
        # Gas
        figure_gas = {p + cmd_move[cmd] for p in figure}
        if self.positions_are_valid(figure_gas):
            figure = figure_gas
        # Fall
        figure_fall = {p - 1 for p in figure}
        if self.positions_are_valid(figure_fall):
            figure = figure_fall
        else:
            self.rocks |= figure
            self.bottom = max(self.bottom, *[p.real + 1 for p in figure])
            return (figure, False)

        return (figure, True)

    def drop_figure(self, figure: Fig, cmds: Iterator[Cmd]) -> Fig:
        figure = {p + self.bottom + 3 + 2j for p in figure}
        for cmd in cmds:
            figure, is_moving = self._move(figure, cmd)
            if not is_moving:
                return figure

    def __repr__(self) -> str:
        height = max((int(p.real) for p in self.rocks), default=1) + 3
        return '\n'.join([
            ''.join(
                ['|'] +
                ['#' if x + y*1j in self.rocks else '.' for y in range(7)] +
                ['|']
            )
            for x in reversed(range(height))
        ] + ['+' + '_' * 7 + '+'])


def part_1(filename: str) -> int:
    chamber = Chamber(set())
    cmds = parse_file(filename)
    cmds = iter(cycle(cmds))
    for i in range(2022):
        chamber.drop_figure(figures[i % len(figures)], cmds)
    return int(chamber.bottom)


print(part_1('test.txt'))
print(part_1('input.txt'))


def part_2(filename: str) -> int:
    chamber = Chamber(set())
    cmds = parse_file(filename)
    cmds = iter(cycle(cmds))
    prev = 0
    res = []
    for i in range(5000):
        _ = chamber.drop_figure(figures[i % len(figures)], cmds)
        res.append(int(chamber.bottom) - prev)
        prev = int(chamber.bottom)

    def find_cycle(l: list) -> list:
        for i in range(len(l)):
            for j in range((len(l) - i) // 2):  # Get at least 2 cycles
                if list(islice(cycle(islice(l, i, j + 1)), len(l) - i)) == l[i:]:
                    return l[:i], l[i:j+1]

    nb_rocks = 1000000000000
    beg, pattern = find_cycle(res)
    quotient, remainder = (
        nb_rocks - len(beg)) // len(pattern), (nb_rocks - len(beg)) % len(pattern)
    return sum(beg) + quotient*sum(pattern) + sum(pattern[:remainder])


print(part_2('test.txt'))
print(part_2('input.txt'))

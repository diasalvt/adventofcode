from itertools import product
from typing import *
import re
from collections import namedtuple, Counter
from tqdm import tqdm

with open('input.txt') as f:
    cmds = f.read().splitlines()
    
Cmd = namedtuple('Cmd', ['action', 'start', 'end'])
Cmds = List[Cmd]
Pos = Tuple[int, int]

def parse_cmds(cmds: List[str]) -> Cmds:
    regex = re.compile(r".*(on|off|toggle) (\d+),(\d+) through (\d+),(\d+)")

    def match_to_cmd(match: re.Match) -> Cmd:
        action, x1, y1, x2, y2 = match.groups()
        return Cmd(action, (int(x1), int(y1)), (int(x2), int(y2)))

    return [match_to_cmd(re.match(regex, s)) for s in cmds]

cmds = parse_cmds(cmds)

def play_cmds(cmds: Cmds) -> Set[Pos]:

    def grid(start: Pos, end: Pos) -> Set[Pos]:
        x1, y1 = start
        x2, y2 = end
        return set(product(range(x1, x2 + 1), range(y1, y2 + 1)))

    on = set()
    for cmd in cmds:
        match cmd:
            case Cmd('on', start, end):
                on |= grid(start, end)
            case Cmd('off', start, end):
                on -= grid(start, end)
            case Cmd('toggle', start, end):
                on ^= grid(start, end)

    return on

print(len(play_cmds([
    Cmd('on', (0, 0), (499, 0)),
    Cmd('toggle', (0, 0), (999, 0)),
    Cmd('off', (499, 499), (500, 500))
])))
print(len(play_cmds(cmds)))


def play_cmds2(cmds: Cmds) -> Counter:

    def grid(start: Pos, end: Pos) -> Set[Pos]:
        x1, y1 = start
        x2, y2 = end
        return set(product(range(x1, x2 + 1), range(y1, y2 + 1)))

    on = Counter()
    for cmd in tqdm(cmds):
        match cmd:
            case Cmd('on', start, end):
                on += Counter(grid(start, end))
            case Cmd('off', start, end):
                on -= Counter(grid(start, end))
            case Cmd('toggle', start, end):
                c = Counter(grid(start, end))
                on += (c + c)

    return on

print(play_cmds2(cmds).total())

from collections import defaultdict
from typing import *
from itertools import islice, takewhile, product, chain
from math import sqrt
import re

Vector = Tuple[int, int]
Grid = Tuple[Vector, Vector]
Traj = Iterable[Tuple[Vector, Vector]]

def sumt(t1, t2):
    return tuple(map(sum, zip(t1, t2)))

def in_grid(pos: Vector, grid: Grid):
    pos_x, pos_y = pos
    (grid_x_min, grid_x_max), (grid_y_min, grid_y_max) = grid
    return (grid_x_min <= pos_x <= grid_x_max) and (grid_y_min <= pos_y <= grid_y_max)

def iter_grid(grid: Grid):
    (grid_x_min, grid_x_max), (grid_y_min, grid_y_max) = grid
    return product(range(grid_x_min, grid_x_max + 1), range(grid_y_min, grid_y_max + 1))

def sign(x):
    if x > 0: return 1
    elif x < 0: return -1
    else: return 0

def traj(initpos: Vector, initvel: Vector) -> Traj:
    p_n = initpos
    v_n = initvel
    while True:
        yield p_n, v_n
        p_n = sumt(p_n, v_n)
        v_n = sumt(v_n, (-sign(v_n[0]), -1))

def traj_intersect_target(traj: Traj, target: Grid):
    return any(in_grid(pos, target) for pos, _ in traj )

def print_traj(traj: Traj, grid: Grid, target: Grid) -> None:
    traj_pos, traj_vel = zip(*takewhile(lambda x: in_grid(x[0], grid), traj))
    start, *rest_traj = traj_pos

    character_display: DefaultDict[Vector, str] = defaultdict(lambda: '.')
    character_display[start] = 'S'
    for pos in iter_grid(target):
        character_display[pos] = 'T'
    for pos in rest_traj:
        if pos in iter_grid(target):
            character_display[pos] = '@'
        else:
            character_display[pos] = '#'

    for y in reversed(range(grid[1][0], grid[1][1] + 1)):
        print(*[character_display[(x, y)] for x in range(grid[0][0], grid[0][1] + 1)])
            
def is_triang(n):
    if n < 0:
        return False
    sqrt_2n = int(sqrt(2*n))
    return 2*n == (sqrt_2n * (sqrt_2n + 1))

def anterior_triang(n):
    return int(sqrt(2 * n))

def triang(n):
    return (n * (n + 1)) / 2

def consecutive_sum(n):
    l = anterior_triang(n) + 1
    for i in range(1, l):
        if (first_term := (n - triang(i - 1))) % i == 0:
            if first_term == i:
                yield 0, i + 1
            yield int(first_term // i), i

def find_vel_y_one_target(source_y, target_y):
    #res = next(filter(is_triang, reversed(range(triang_strictly_below(source_y - target_y) + 1))))
    res = (source_y - target_y) - 1
    return res

def find_vel_y(source_y, target_y_range):
    target_y_min, target_y_max = target_y_range
    return max(find_vel_y_one_target(source_y, y) for y in range(target_y_min, target_y_max + 1))

def find_all_vel_y_one_target(source_y, target_y):
    depth = source_y - target_y
    d = defaultdict(set)
    for v, i in consecutive_sum(depth):
        d[2 * v - 1 + i].add(v - 1)
        d[i].add(-v)
    return d

def find_all_vel_x_one_target(source_x, target_x):
    distance = target_x - source_x
    d = defaultdict(set)
    for v, i in consecutive_sum(distance):
        d[i].add(v + i - 1)
    return d

def find_all_vel_one_target(source, target):
    source_x, source_y = source
    x, y = target
    res = set()

    f_y = find_all_vel_y_one_target(source_y, y)
    f_x = find_all_vel_x_one_target(source_x, x)
    for step_x, set_v_x in f_x.items():
        for v_x in set_v_x:
            if triang(v_x) == x:
                for step_y, set_v_y in f_y.items():
                    if step_y >= step_x:
                        res |= set(product([v_x], set_v_y))
            else:
                res |= set(product(set_v_x, f_y[step_x]))

    return res 

def find_all_vel(source, target):
    source_x, source_y = source
    target_x, target_y = target

    res = set()
    for x, y in iter_grid(target):
        res |= find_all_vel_one_target(source, (x, y))
    return res

grid = ((0, 30), (-10, 45))
target = ((20000, 30000), (-10000, -5000))
source = (0, 0)

with open('input17.txt') as f:
    first_row = next(f)

target_x_min, target_x_max, target_y_min, target_y_max = [int(e) for e in re.findall(r"-*\d+", first_row)]
target_file = (target_x_min, target_x_max), (target_y_min, target_y_max)


#print(len(find_all_vel((0, 0), target_file)))
print(len(find_all_vel((0, 0), target)))
from typing import *
from itertools import chain, tee, product, combinations
import re
from functools import reduce
from operator import mul

Range = Tuple[int, int]
Point = Tuple[int, ...]
Cube = Tuple[Range, Range, Range]
Sign = int

def pairwise(it: Iterable):
    it, it2 = tee(it, 2)
    _ = next(it2)
    return zip(it, it2)

def between(coord: int, range: Range):
    beg, end = range
    return beg <= coord <= end

def strictly_between(coord: int, range: Range):
    beg, end = range
    return beg < coord < end

def range_equal(range_a: Range, range_b: Range):
    return all(ai == bi for ai, bi in zip(range_a, range_b))

def range_in(range_a: Range, range_b: Range):
    (beg_a, end_a), (beg_b, end_b) = range_a, range_b
    return between(beg_a, range_b) and between(end_a, range_b)

def range_outside(range_a: Range, range_b: Range):
    (beg_a, end_a), (beg_b, end_b) = range_a, range_b
    return (end_a <= beg_b) or (beg_a >= end_b)

def range_collision(range_a: Range, range_b: Range):
    (beg_a, end_a), (beg_b, end_b) = range_a, range_b
    return between(beg_b, range_a) or between(end_b, range_a) or range_in(range_a, range_b) or range_in(range_b, range_a)

def collision(cube_a: Cube, cube_b: Cube):
    return all(range_collision(r_a, r_b) for r_a, r_b in zip(cube_a, cube_b))

def range_minus(r_a: Range, r_b: Range):
    points = chain(r_a, r_b)
    segments = list(pairwise(sorted(points)))
    selected_segments = [r for r in segments if range_in(r, r_a) and range_outside(r, r_b)]
    a_minus_b = set((beg + between(beg, r_b), end - between(end, r_b)) for beg, end in selected_segments if beg != end)

    return a_minus_b

def range_and(r_a: Range, r_b: Range):
    points = chain(r_a, r_b)
    segments = list(pairwise(sorted(points)))
    selected_segments = [r for r in segments if range_in(r, r_a) and range_in(r, r_b)]
    a_inter_b = set((beg, end) for beg, end in selected_segments)

    if len(a_inter_b) > 1:
        cleaned_a_inter_b = set((beg, end) for beg, end in a_inter_b if beg != end)
    else:
        cleaned_a_inter_b = a_inter_b
    return cleaned_a_inter_b


c1 = (
    (0, 5),
    (2, 4),
    (12, 14)
)
c12 = (
    (1, 3),
    (1, 3),
    (1, 3)
)
c13 = (
    (4, 5),
    (4, 5),
    (4, 5)
)
c2 = (
    (1, 2),
    (1, 3),
    (3, 3)
)
c3 = (
    (10, 12),
    (10, 13),
    (30, 33)
)

#print(range_minus(c1[0], c2[0]))
#print(range_minus(c1[0], c2[1]))
#print(range_minus(c1[2], c2[1]))
#print(range_minus(c1[0], c2[2]))
#print(range_and(c1[0], c2[0]))
#print(range_and(c1[0], c2[1]))

def cube_and(cube_a: Cube, cube_b: Cube):
    if not collision(cube_a, cube_b):
        return set()
    
    ranges = [range_and(r_a, r_b) for r_a, r_b in zip(cube_a, cube_b)] 
    return set(product(*ranges))

def cube_minus(cube: Cube, substracted_cube: Cube):
    if not collision(cube, substracted_cube):
        return {cube}
    ranges_outside_and_inside = [range_minus(r_a, r_b) | range_and(r_a, r_b) for r_a, r_b in zip(cube, substracted_cube)] 
    return set(product(*ranges_outside_and_inside)) - cube_and(cube, substracted_cube)

def cube_in(cube_a, cube_b):
    return all(range_in(r_a, r_b) for r_a, r_b in zip(cube_a, cube_b))

#print(cube_minus(c1, c2))
#a = cube_minus(((-46, 7), (-6, 46), (-50, -1)), ((-48, -32), (26, 41), (-47, -37)))
#print(len(a))
#print(a)


#print(cube_and(((18, 23), (-19, -9), (-3, 13)), ((18, 30), (-19, -9), (-2, 12))))

def search_collision(cube: Cube, cubes: Iterable[Cube]):
    return set(c for c in cubes if collision(cube, c))

def search_collision_with_sign(cube: Cube, cubes: Iterable[Tuple[Cube, Sign]]):
    return [t for t in cubes if collision(cube, t[0])]

input = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
"""

input = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
"""

with open("input22.txt") as f:
    file_input = [row.strip() for row in f]
instructions = []
patterns = [re.compile(fr"{axis}=(-?\d+)..(-?\d+)") for axis in ['x', 'y', 'z']]
for row in input.strip().split('\n'):
#for row in file_input[:20]:
    state, coords = row.split()
    instructions.append((state, tuple(tuple(map(int, re.search(p, coords).group(1, 2))) for p in patterns)))

#instructions = instructions[:12] 

def build_on_cubes(instructions):
    on_cubes = set()
    for state, cube in instructions:
        if state == 'on':
            on_cubes.add(cube)
        else:
            colliding_cubes = search_collision(cube, on_cubes)
            new_cubes = set()
            for c in colliding_cubes:
                new_cubes.update(cube_minus(c, cube))
            on_cubes -= colliding_cubes
            on_cubes |= new_cubes

    return on_cubes

def volume_cube(cube: Cube):
    if len(cube) == 0:
        return 0
    else:
        return reduce(mul, map(lambda x: x[1] - x[0] + 1, cube))

def grid_volume(instructions):
    grid_on: Set[Point] = set()
    for state, cube in instructions:
        ranges = map(lambda x: range(x[0], x[1] + 1), cube)
        if state == 'on':
            for x, y, z in product(*ranges):
                grid_on.add((x, y, z))
        else:
            for x, y, z in product(*ranges):
                grid_on.discard((x, y, z))

    return len(grid_on)

def volume(cubes: Iterable[Cube]):
    seen_cubes_and_intersections: List[Tuple[Cube, Sign, int]] = []
    for i, c1 in enumerate(cubes):
        for c2, sign, count in search_collision_with_sign(c1, seen_cubes_and_intersections):
            if len(inter := cube_and(c1, c2)) > 0:
                cube_inter = inter.pop()
                seen_cubes_and_intersections.append((cube_inter, -sign, count + 1))
        seen_cubes_and_intersections.append((c1, 1, 1))

    total_v = 0
    for c, sign, count in seen_cubes_and_intersections:
        total_v += sign*volume_cube(c)
    return total_v

on_cubes = build_on_cubes(instructions)
print(volume(on_cubes))
            
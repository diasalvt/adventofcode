from itertools import takewhile, product, starmap, chain, islice, groupby, combinations, permutations
from operator import le, mul, ge
from collections import defaultdict
from functools import reduce
from typing import *
from statistics import mean
import time

with open("input19.txt") as f:
    def parse_stack(f):
        while True:
            try:
                next(f)
                stack = [tuple(map(int, p.strip().split(',')))
                         for p in takewhile(lambda x: x != "\n", f)]
                yield stack
            except StopIteration:
                return

    stacks = list(parse_stack(f))

Point = Tuple[int, ...]
Points = Set[Point]

def pairwise(it: Sequence):
    for a, b in zip(it, it[1:]):
        yield a, b

def group(points: Point):
    s_points = sorted(points)
    p_0, *p = s_points[0]
    res = [tuple(p)]
    for (first_prev_p, *prev_p), (first_p, *p) in pairwise(s_points):
        p_0 = first_p
        if first_prev_p != first_p:
            yield first_prev_p, res
            res = [tuple(p)]
        else:
            res.append(tuple(p))
    yield p_0, res

test = [(0, 1, 2), (0, 1, 3), (1, 1, 0), (1, 1, 2), (2, 3, 4)]
#print(list(group(test)))
#print(list(groupby(test, key=lambda x: x[0])))

def space_tree(points: Point):
    shape = len(points[0])
    
    values, groups = zip(*group(points))
    if shape == 1:
        return (values, None)
    else:
        groups = {v: space_tree(g) for v, g in zip(values, groups)}
        return (values, groups)

def tk_le(it, v):
    return takewhile(lambda x: x <= v, it)

def r_search(space_tree, path, thresholds):
    t_0, *t = thresholds
    values, groups = space_tree
    selected_val = list(tk_le(values, t_0))
    if groups is None:
        if len(selected_val):
            return [path + (v,) for v in selected_val]
        return [] 
    res = []
    for v in selected_val:
        res += r_search(groups[v], path + (v,), t)
    return res

def search(space_tree, thresholds):
    return frozenset(r_search(space_tree, (), thresholds))

def merge_sorted(list_a, list_b):
    it_a, it_b = iter(list_a), iter(list_b)

    def keep_lower(a, b):
        if a is None:
            return False
        if b is None:
            return True
        return a <= b

    a, b = next(it_a, None), next(it_b, None)
    while (a is not None) or (b is not None):
        if keep_lower(a, b):
            yield a
            a = next(it_a, None)
        else:
            yield b
            b = next(it_b, None)

def l_merge(l):
    return reduce(merge_sorted, l)

def unique_sorted(it):
    prev = None
    for e in it:
        if (prev is None) or (e != prev): 
            yield e
            prev = e
    return

def find_x(it, size):
    slice = list(islice(it, size - 1, size + 1))
    if len(slice) == 0:
        return None
    elif len(slice) == 1:
        return slice[0]
    else:
        a, b = slice
        return a if a != b else None

#print(list(islice(merge_sorted([1, 2, 6, 7, 9], [0, 1, 3, 7]), 5)))
#print(list(unique_sorted(merge_sorted([1, 2, 6, 7, 9], [0, 1, 3, 7]))))
#print(find_x(merge_sorted([1, 2, 6, 7, 9], [0, 1, 3, 7]), 6))
#print(test)
#print(space_tree(test))
#print(search(space_tree(test), (1, 1, 2)))

def subspaces_of_size(l_tree, size):
    l_values, l_groups = zip(*l_tree)

    if l_groups[0] is None:
        if (x := find_x(l_merge(l_values), size=size)) is not None:
            return [(x,)]
        else:
            return []

    else:
        res = []
        for x in unique_sorted(l_merge(l_values)):
            next_l_tree = [groups[v] for values, groups in l_tree for v in tk_le(values, x)]
            subsearch = subspaces_of_size(
                next_l_tree,
                size
            )
            res += [(x,) + e for e in subsearch]
        return res

def compose2(f, g):
    def r(*args, **kwargs):
        return f(g(*args, **kwargs))
    return r

def compose(l_f):
    return reduce(compose2, l_f)

def power_f(f, n):
    if n == 0:
        return lambda x: x
    return compose([f]*n)

def _basic_perm(point):
    x, y, z = point
    return z, x, y

def _n_perm(n):
    perm = list(permutations(range(3)))[n]
    invperm, _ = zip(*sorted(zip(range(3), perm), key=lambda x: x[1]))
    def transfo(point):
        return tuple(point[idx] for idx in perm)
    def invtransfo(point):
        return tuple(point[idx] for idx in invperm)

    return transfo, invtransfo

def _inv_basic_perm(point):
    x, y, z = point
    return y, z, x

class Permutation:
    def __init__(self, n):
        self.perm, self.invperm = _n_perm(n)

    def __call__(self, v):
        return self.perm(v)

    def inv(self, v):
        return self.invperm(v)

def _rot(signs):
    s_x, s_y, s_z = signs
    def r(point):
        x, y, z = point 
        return s_x*x, s_y*y, s_z*z
    return r

class Rotation:
    def __init__(self, signs):
        s_x, s_y, s_z = signs
        self.rot = _rot(signs)
        self.invrot = _rot(signs)

    def __call__(self, v):
        return self.rot(v)

    def inv(self, v):
        return self.invrot(v)

def points_subspaces(points, size):
    perm_param = range(3)
    rot_param = product(*[[1, -1]]*3)
    found_subspaces = set()
    for p, r in product(perm_param, rot_param):
        permutation = Permutation(p)
        rotation = Rotation(r)
        t, inv_t = compose([permutation, rotation]), compose([rotation.inv, permutation.inv])


        t_points = [t(p) for p in points]
        invt_points = [rotation.inv(p) for p in points]
        s_tree = space_tree(t_points)
        subspaces = {search(s_tree, t) for t in subspaces_of_size([s_tree], size)}
        found_subspaces |= {frozenset(inv_t(p) for p in subspace) for subspace in subspaces}

    return found_subspaces

def bruteforce(points, size):
    def in_subspace(p, t, sides):
        return all([s_i*p_i <= s_i*t_i for p_i, t_i, s_i in zip(p, t, sides)])

    x_v, y_v, z_v = zip(*points)

    for x in set(x_v):
        for y in set(y_v):
            for z in set(z_v):
                for s in product(*[[1, -1]]*3):
                    selected_points = frozenset([p for p in points if in_subspace(p, (x, y, z), s)])
                    if len(selected_points) == size:
                        yield selected_points

def brute(points, size):
    return set(bruteforce(points, size))

#s_tree = space_tree(test)
#subspaces = subspaces_of_size([s_tree], 3)
#for thresholds in subspaces:
#    print(thresholds)
#    print(search(s_tree, thresholds))


def fingerprint_points(points):
    def dist(x, y):
        return sum((xi - yi)**2 for xi, yi in zip(x, y))

    def inter_dist(l):
        return sum(dist(x, y) for x in l for y in l)
    
    return inter_dist(points)

def fingerprint_subspace(subspaces):
    d = defaultdict(list)
    for points in subspaces:
        d[fingerprint_points(points)].append(points)
    res = {k: v for k, v in d.items() if len(v) >= 2}
    return res

def check_transfo(points_a, points_b):
    def translate(point, vector):
        return tuple(p + v for p, v in zip(point, vector))

    origin = sorted(points_a)[0]
    perm_param = range(6)
    rot_param = list(product(*[[1, -1]]*3))
    for p, r in product(perm_param, rot_param):
        permutation = Permutation(p)
        rotation = Rotation(r)
        t, inv_t = compose([rotation, permutation]), compose([permutation.inv, rotation.inv])

        t_points = [t(p) for p in points_b]
        t_origin = sorted(t_points)[0]
        translation = tuple(a - b for a, b in zip(origin, t_origin))

        t_points = set([translate(p, translation) for p in t_points])
        res = points_a.symmetric_difference(t_points)
        if len(res) == 0:
            transfo = lambda x: translate(t(x), translation)
            inv_transfo = lambda x: inv_t(translate(x, tuple(-e for e in translation)))
            return (p, r, translation, transfo, inv_transfo)
    return None

subspaces = [points_subspaces(s, 12) for s in stacks]
fp = fingerprint_subspace(chain.from_iterable(subspaces))
subspace_to_stack = {subspace: i for i, l_subspaces in enumerate(subspaces) for subspace in l_subspaces}

associated_subspaces = []
for _, v in fp.items():
    for a, b in combinations(v, 2):
        res = check_transfo(a, b)
        if res:
            _, _, _, t, inv_t = res
            i, j = subspace_to_stack[a], subspace_to_stack[b]
            associated_subspaces.append((j, i, t))
            associated_subspaces.append((i, j, inv_t))

to_be_converted = set(range(1, len(stacks)))
conversion = {
    0: lambda x: x
}

while len(to_be_converted) > 0:
    for j, i, t in associated_subspaces:
        if (i in conversion) and not (j in conversion):
            conversion[j] = compose([conversion[i], t])
            to_be_converted -= {j}

all_points = set(stacks[0])
for i, s in enumerate(stacks[1:]):
    all_points |= set(conversion[i + 1](p) for p in s)

print(len(all_points))
origins = [v((0, 0, 0))for k, v in conversion.items()]

def manhattan(pair):
    a, b = pair
    return sum(abs(ai - bi) for ai, bi in zip(a, b))

print(max(map(manhattan, combinations(origins, 2))))

#for s in stacks[1:]:
#    r = points_subspaces(s, 12)
#    f = set(fingerprint(points) for points in r)
#    print(len(f_0.intersection(f)))

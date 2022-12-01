from typing import Tuple
from functools import reduce
from itertools import starmap, combinations
from operator import mul

with open('input.txt') as f:
    size_data = f.readlines()
    sizes = [list(map(int, s.split('x'))) for s in size_data]

Size = Tuple[int, int, int]

def paper(size: Size) -> int:
    face_size = combinations(size, 2)
    face_surface = list(starmap(mul, face_size))
    wrapping_paper = 2*sum(face_surface) + min(face_surface)
    return wrapping_paper

def test_paper():
    assert paper((1, 1, 10)) == 43

def ribbon(size: Size) -> int:
    face_size = combinations(size, 2)
    face_perimeter = list(starmap(lambda x, y: 2*(x+y), face_size))
    min_perimeter = min(face_perimeter)
    return min_perimeter + reduce(mul, size)

def test_ribbon():
    assert ribbon((2, 3, 4)) == 34
    assert ribbon((1, 1, 10)) == 14

total_paper = sum(map(paper, sizes))
total_ribbon = sum(map(ribbon, sizes))

print(total_paper)
print(total_ribbon)
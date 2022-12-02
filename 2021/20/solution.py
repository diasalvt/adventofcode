import numpy as np
from io import StringIO
from scipy.signal import convolve2d

def str_to_intarr(s):
    return [0 if si == '.' else 1 for si in s]

algo = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#""".replace('\n', '')

txt_image = """#..#.
#....
##..#
..#..
..###"""

with open("input20.txt") as f:
    algo = next(f)
    _ = next(f)
    txt_image = ''.join(list(f))

algo = str_to_intarr(algo)

img = np.genfromtxt(
    StringIO(txt_image), delimiter=1, 
    comments='@', dtype=str
)
img = (img == "#").astype(int)
mat_power_of_two = np.array([[2**(i*3+j) for j in range(3)] for i in range(3)])
vectorize_get_item = np.vectorize(lambda x: algo[x])

def steps(img, n):
    for i in range(n):
        img = np.pad(img, (2, 2), mode="constant", constant_values=(0 if i % 2 == 0 else 1))
        indexes = convolve2d(img, mat_power_of_two, mode='valid')
        img = vectorize_get_item(indexes)
    return img

print(np.count_nonzero(steps(img, 50)))
import re
import numpy as np
from typing import Union
from itertools import combinations, chain
from sympy import Eq, Symbol, solve


Vec = tuple[float]
Path = tuple[Vec, Vec]


def load(filename: str) -> list[Path]:
    data = []
    with open(filename) as f:
        for row in f.read().splitlines():
            px, py, pz, vx, vy, vz = map(int, re.findall(r'-?\d+', row))
            data.append(((px, py, pz), (vx, vy, vz)))
    return data


def intersection(
    path_a: Path, path_b: Path
) -> Union[None, 'all', Vec]:
    (p_a, v_a), (p_b, v_b) = path_a, path_b
    V = np.array([v_a, [-v for v in v_b]]).transpose()
    P = np.subtract(np.array([p_b]), np.array([p_a])).transpose()

    try:
        return np.linalg.solve(V, P)
    except np.linalg.LinAlgError:
        # Line overlap
        if np.linalg.matrix_rank(np.concatenate((V, P), axis=1)) == 1:
            return 'all'
        return None


_LOWER = 200000000000000
_HIGHER = 400000000000000


def is_valid(
    path_a: Path, path_b: Path, low_high: tuple[int, int]
) -> bool:
    inter_res = intersection(path_a, path_b)

    match inter_res:
        case np.ndarray():
            pos = tuple(
                inter_res[0, 0] * v_i + p_i for p_i, v_i in zip(*path_a)
            )
            return (
                np.all(inter_res > 0)
                and all(
                    low_high[0] <= p_i <= low_high[1]
                    for p_i in pos
                )
            )
        case 'all':
            return True
        case None:
            return False


def dim2d(data: list[Path]) -> list[Path]:
    return [((px, py), (vx, vy)) for (px, py, _), (vx, vy, _) in data]


test = dim2d(load('test.txt'))
paths = dim2d(load('input.txt'))

print(
    sum(is_valid(*pair, (_LOWER, _HIGHER)) for pair in combinations(paths, 2))
)


def generate_equation(
    path: Path, p_symb: tuple[Symbol], v_symb: tuple[Symbol],
    i: int
) -> tuple[Symbol, list[Eq]]:
    position, vel = path
    t_i = Symbol(f't_{i}')
    return t_i, [
        Eq(p_i - p_symb_i + t_i * (v_i - v_symb_i), 0)
        for p_i, v_i, p_symb_i, v_symb_i in zip(position, vel, p_symb, v_symb)
    ]


def equations(data: list[Path]) -> tuple[list[Symbol], list[Eq]]:
    p_symb = [Symbol(f'p_{s}') for s in ['x', 'y', 'z']]
    v_symb = [Symbol(f'v_{s}') for s in ['x', 'y', 'z']]

    t_symb, eqs = zip(*(
        generate_equation(path, p_symb, v_symb, i)
        for i, path in enumerate(data)
    ))
    eqs = list(chain.from_iterable(eqs))
    t_symb = list(t_symb)

    return p_symb + v_symb + t_symb, eqs


symbols, eqs = equations(load('input.txt')[:3])
print(sum(solve(eqs, symbols)[0][:3]))

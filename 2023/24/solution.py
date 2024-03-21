import re
import numpy as np
from typing import Union

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
    V = np.array([v_a, v_b]).transpose()
    P = np.subtract(np.array([p_b]), np.array([p_a])).transpose()

    print(V, P)
    try:
        return np.linalg.solve(V, P)
    except np.linalg.LinAlgError:
        # Line overlap
        if np.linalg.matrix_rank(np.concatenate((V, P), axis=1)) == 1:
            return 'all'
        return None


_LOWER = 200000000000000
_HIGHER = 400000000000000


def is_valid(path_a, path_b, inter_res) -> bool:
    match inter_res:
        case 'all':
            return True
        case None:
            return False
        case _:
            pos = tuple(
                inter_res[0, 0] * v_i + p_i for p_i, v_i in zip(*path_a)
            )
            print(pos)
            return all(
                _LOWER <= p_i <= _HIGHER
                for p_i in pos
            )


def dim2d(data: list[Path]) -> list[Path]:
    return [((px, py), (vx, vy)) for (px, py, _), (vx, vy, _) in data]


test = dim2d(load('test.txt'))
print(is_valid(test[0], test[1], intersection(test[0], test[1])))

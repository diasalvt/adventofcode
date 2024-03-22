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
    path_a: Path, path_b: Path, inter_res: np.array, low_high: tuple[int, int]
) -> bool:
    match inter_res:
        case 'all':
            return True
        case None:
            return False
        case _:
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


def dim2d(data: list[Path]) -> list[Path]:
    return [((px, py), (vx, vy)) for (px, py, _), (vx, vy, _) in data]


test = dim2d(load('test.txt'))

for t in test[1:]:
    print(is_valid(test[0], t, intersection(test[0], t), (7, 27)))

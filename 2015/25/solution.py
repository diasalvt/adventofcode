from itertools import chain
from typing import *


def transform(x: int) -> int:
    """
    Rule to generate next code
    """

    return (x * 252533) % 33554393

Pos = Tuple[int, int]
def code_positions(stop: int) -> Generator[Pos, None, None]:
    for diag in range(1, stop):
        for x in reversed(range(1, (diag + 1))):
            yield (x, diag - x + 1)

print(list(code_positions(10)))

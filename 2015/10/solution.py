from typing import Iterable, Generator
from itertools import chain


test = '111221'
inp = '1113222113'

def groups(iterable: Iterable) -> Generator[list, None, None]:
    prev = None
    start = True
    current_stack = []
    for e in iterable:
        if e == prev:
            current_stack.append(e)
        else:
            if start:
                start = False
            else:
                yield current_stack
            current_stack = [e]
        prev = e
    yield current_stack


def transfo(s: str) -> str:
    g = list(groups(s))
    count_and_value = zip(
        map(lambda x: str(len(x)), g),
        map(lambda x: x[0], g)
    )
    return ''.join(chain.from_iterable(count_and_value))


def play(start: str, nb: int = 40):
    result = start
    for i in range(nb):
        result = transfo(result)

    return result

print(len(play(inp)))
print(len(play(inp, 50)))

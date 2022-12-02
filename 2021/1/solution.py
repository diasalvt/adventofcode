from functools import reduce
from itertools import islice, filterfalse
from collections import deque
from typing import Iterable
import time
import random
from contextlib import contextmanager

def sol_1():
    with open("input1.txt") as f:
        values = (int(row) for row in f)

        res = reduce(lambda x, y: (x[0] + (y > x[1]), y), values, (0, 0))[0] - 1
        print(res)

def sol_2():
    with open("input1.txt") as f:
        values = (int(row) for row in f)

        res = count_increase(exterior_window(values))
        print(res)
       
def exterior_window(values: Iterable, size=3):
    it = iter(values)
    # Keep a memory of `size` values
    memory = [next(it) for _ in range(size)]
    for i, elem in enumerate(it):
        yield(memory[i % size], elem)
        memory[i % size] = elem
        
def ext_window(values: Iterable, size=3):
    iterator = iter(values)
    memory = deque(islice(iterator, size))
    
    for elem in iterator:
        memory.append(elem)
        yield (memory.popleft(), elem)

def count_increase(values: Iterable):
    return sum(1 for elem in filter(lambda x: x[1] > x[0], values))

@contextmanager
def time_context(name):
    start_time = time.time()
    yield
    elapsed_time = time.time() - start_time
    print('[{}] finished in {} ms'.format(name, int(elapsed_time * 1_000)))

sol_2()
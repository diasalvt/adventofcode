from collections import defaultdict
import re
from typing import Tuple, DefaultDict
from itertools import chain, cycle, zip_longest, tee

pattern = re.compile(r'(\d+),(\d+)\s*->\s*(\d+),(\d+)')

Block = Tuple[int, int]
Line = Tuple[Block, Block]

def unsorted_range(a, b):
    if a < b:
        return range(a, b + 1)
    else:
        return reversed(range(b, a + 1))

def is_vertical(line):
    block1, block2 = line
    x1, y1, x2, y2 = chain(block1, block2)
    return y1 == y2

def is_horizontal(line):
    block1, block2 = line
    x1, y1, x2, y2 = chain(block1, block2)
    return x1 == x2

def is_diagonal(line):
    block1, block2 = line
    x1, y1, x2, y2 = chain(block1, block2)
    return abs(x1 - x2) == abs(y1 - y2)

def zip_cycle(*iterables):
    iterables, cycle_iterables = zip(*[tee(iterable, 2) for iterable in iterables])

    for values_with_null, values_fill_cycle in zip(
        zip_longest(*iterables), 
        zip(*[cycle(iterable) for iterable in cycle_iterables])):
        yield values_fill_cycle

def line_to_blocks(line):
    block1, block2 = line
    x1, y1, x2, y2 = chain(block1, block2)

    for x, y in zip_cycle(unsorted_range(x1, x2), unsorted_range(y1, y2)):
            yield (x, y)

def sol1():
    with open('input5.txt') as f:
        def file_to_lines(file):
            for line in file:
                x1, y1, x2, y2 = map(int, pattern.match(line).groups())
                yield ((x1, y1), (x2, y2))

        lines = file_to_lines(f)

        block_usage: DefaultDict[Block, int] = defaultdict(int)
        blocks_over_2 = set()

        vertical_or_horizontal = lambda x: is_vertical(x) or is_horizontal(x)
        for line in filter(vertical_or_horizontal, lines):
            for block in line_to_blocks(line):
                block_usage[block] += 1
                if block_usage[block] >= 2:
                    blocks_over_2.add(block)

        print(len(blocks_over_2))

def sol2():
    with open('input5.txt') as f:
        def file_to_lines(file):
            for line in file:
                x1, y1, x2, y2 = map(int, pattern.match(line).groups())
                yield ((x1, y1), (x2, y2))
    
        lines = file_to_lines(f)
    
        block_usage: DefaultDict[Block, int] = defaultdict(int)
        blocks_over_2 = set()
    
        authorized = lambda x: is_vertical(x) or is_horizontal(x) or is_diagonal
        for line in filter(authorized, lines):
            for block in line_to_blocks(line):
                block_usage[block] += 1
                if block_usage[block] >= 2:
                    blocks_over_2.add(block)
    
        print(len(blocks_over_2))

sol1()
sol2()
from collections import defaultdict, Counter
from itertools import filterfalse, islice
from typing import Sequence, Iterable
from functools import reduce

def bits_to_int(bits: Sequence):
    return reduce(lambda x, y: 2*x + y, bits, 0)

def sol1():
    with open("input3.txt") as f:
        counts = defaultdict(int)

        for i, row in enumerate(f):
            for j, bit in enumerate(row[:-1]):
                counts[j] += int(bit)

        print(i)
        most_common = [int(counts[k] > i // 2) for k in sorted(counts.keys())]
        least_common = [int(counts[k] <= i // 2) for k in sorted(counts.keys())]

        print(bits_to_int(most_common) * bits_to_int(least_common))

def most_common_bit(bits: Iterable, *, equality_case_default=1):
    return int(reduce(lambda x, y: x + (1 if y == 1 else -1), bits, 0) > (0 - equality_case_default))

def least_common_bit(bits: Iterable, *, equality_case_default=0):
    xor_1 = lambda x: 0 if x else 1
    return xor_1(most_common_bit(bits, equality_case_default=xor_1(equality_case_default)))

def nth(iterable: Iterable, n: int):
    return next(islice(iterable, n, None))

def sol2():
    with open("input3.txt") as f:
        bits_sequence = [[int(bit) for bit in row[:-1]] for row in f]

        def rating(bits_sequence: Sequence, *, bit_selection=most_common_bit):
            def filter_col_i(bits_sequence, i):
                col_i = nth(zip(*bits_sequence), i)
                return [bits for bits in bits_sequence if bits[i] == bit_selection(col_i)]

            i = 0
            while(len(bits_sequence) > 1):
                bits_sequence = filter_col_i(bits_sequence, i)
                i += 1

            return bits_sequence[0]

        oxygen, co2 = rating(bits_sequence), rating(bits_sequence, bit_selection=least_common_bit)
        print(oxygen, co2)
        print(bits_to_int(oxygen)*bits_to_int(co2))
    
sol2()

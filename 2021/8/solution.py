from itertools import chain, compress
from typing import Callable, Any, Iterable, List
from collections import defaultdict
from functools import reduce
import numpy as np


def quantify(fun: Callable[[Any], bool], iterable: Iterable[Any]):
    return sum(map(fun, iterable))


def groupby(iterable: Iterable, fun: Callable):
    d = defaultdict(list)
    for elem in iterable:
        d[fun(elem)].append(elem)

    return ((elements, grouping_key) for grouping_key, elements in d.items())


def sol1():
    with open("input8.txt") as f:
        codes = [tuple(part.split() for part in row.split('|')) for row in f]
        signals, outputs = zip(*codes)

        def is_1_4_7_8(x): return len(x) in [2, 3, 4, 7]
        print(quantify(is_1_4_7_8, chain.from_iterable(outputs)))

letters = 'abcdefg'
digit_segments = {
    0: frozenset(['a', 'b', 'c', 'e', 'f', 'g']),
    1: frozenset(['c', 'f']),
    2: frozenset(['a', 'c', 'd', 'e', 'g']),
    3: frozenset(['a', 'c', 'd', 'f', 'g']),
    4: frozenset(['b', 'c', 'd', 'f']),
    5: frozenset(['a', 'b', 'd', 'f', 'g']),
    6: frozenset(['a', 'b', 'd', 'e', 'f', 'g']),
    7: frozenset(['a', 'c', 'f']),
    8: frozenset(['a', 'b', 'c', 'd', 'e', 'f', 'g']),
    9: frozenset(['a', 'b', 'c', 'd', 'f', 'g']),
}
segments_digit = {v: k for k, v in digit_segments.items()}

def build_permutation_matrix(signals):

    def vectorize(s: Iterable) -> List[bool]:
        return [l in s for l in letters]

    nb_segments = len(letters)
    digit_segment_vector = {digit: vectorize(segments)
                            for digit, segments in digit_segments.items()}

    initial_array = np.array(
        [vector for _, vector in digit_segment_vector.items()]).transpose()

    permutation_matrix = np.ones((len(letters), len(letters)))

    for signals, nb_signals in sorted(groupby(signals, len), key=lambda x: x[1]):
        vectorized_signals = np.array(
            [vectorize(signal) for signal in signals])
        vectorized_candidates = np.array([vector
                                          for digit, vector in digit_segment_vector.items() if sum(vector) == nb_signals])

        compress_signals = np.all(vectorized_signals, axis=0)
        
        compress_candidates = np.all(vectorized_candidates, axis=0)

        mask = np.ones((nb_segments, nb_segments)) == 1
        for i, value in enumerate(compress_signals):
            if len(signals) == len(vectorized_candidates) or (value == False):
                mask[i] = compress_candidates == value

        permutation_matrix = np.logical_and(mask, permutation_matrix)
        permutation_matrix = unique_one_constraint(permutation_matrix)
    
    return permutation_matrix.transpose()

def decode(signals, new_signal):
    permutation_matrix = build_permutation_matrix(signals)
    translation = {next(compress(letters, vector)): letter for letter, vector in zip(letters, permutation_matrix)}
    return segments_digit[frozenset([translation[new_letter] for new_letter in new_signal])]

def unique_one_constraint_over_row(matrix: np.array) -> np.array:
    """Once a unique True is found in a row force False in the column
    Args:
        matrix (np.array): Current matrix
    Returns:
        np.array: Matrix with less ones
    """
    # To find unique True in col or row
    sum_rows, sum_cols = np.sum(matrix, axis=1), np.sum(matrix, axis=0)
    for row_index_unique_one in np.nonzero(sum_rows == 1)[0]:
        col_index_to_reset = np.nonzero(matrix[row_index_unique_one])[0][0]
        matrix[:, col_index_to_reset] = np.array(
            [i == row_index_unique_one for i in range(matrix.shape[0])])

    return matrix

def unique_one_constraint(matrix):
    """ If a True is identify in a column or a row we can resolve the transpose vector.
    We do this iteratively because new False are introduced.
    """
    sum_rows, sum_cols = np.sum(matrix, axis=1), np.sum(matrix, axis=0)
    total_sum = np.sum(matrix)
    decrease = True
    while decrease and (sum(sum_rows == 1) + sum(sum_cols == 1)) > 0:
        matrix = unique_one_constraint_over_row(matrix)
        matrix = unique_one_constraint_over_row(matrix.transpose()).transpose()
        sum_rows, sum_cols = np.sum(matrix, axis=1), np.sum(matrix, axis=0)
        new_sum = np.sum(matrix)
        decrease = total_sum > new_sum
        total_sum = new_sum
    return matrix

def sol2():
    with open("input8.txt") as f:
        codes = [tuple(part.split() for part in row.split('|')) for row in f]

        def to_number(list_digit):
            return reduce(lambda x, y: x*10 + y, list_digit)

        def signal_to_number(signals, outputs):
            return to_number([decode(signals, new_signal) for new_signal in outputs])

        result = 0
        for i, (signals, outputs) in enumerate(codes):
            result += signal_to_number(signals, outputs)

        print(result)

sol2()
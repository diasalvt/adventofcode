import numpy as np
from typing import List, Set, DefaultDict, Dict
from collections import defaultdict
from itertools import islice, repeat
from functools import reduce
import operator

test_input = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""


def neighbours(matrix, i, j):
    all_neighbours = [(i-1, j), (i, j-1), (i, j+1), (i+1, j)]
    possible_neighbours = filter(lambda x: ((0 <= x[0] < matrix.shape[0]) and
                                            (0 <= x[1] < matrix.shape[1])),
                                 all_neighbours)
    return (matrix[i, j] for i, j in possible_neighbours)


def up_and_left(matrix, i, j):
    all_neighbours = [(i-1, j), (i, j-1)]
    possible_neighbours = filter(lambda x: ((0 <= x[0] < matrix.shape[0]) and
                                            (0 <= x[1] < matrix.shape[1])),
                                 all_neighbours)
    return (matrix[i, j] for i, j in possible_neighbours)


def sol1():
    with open("input9.txt") as f:
        heights = np.array([list(map(int, row.strip())) for row in f])
        #heights = np.array([list(map(int, row.strip())) for row in test_input.strip().split('\n')])

        result = np.zeros(heights.shape)
        for i, j in np.ndindex(result.shape):
            result[i, j] = heights[i, j] <= min(neighbours(heights, i, j))

        print(np.sum(heights[result == 1]) + len(heights[result == 1]))


def sol2():
    with open("input9.txt") as f:
        heights = np.array([list(map(int, row.strip())) for row in f])

        id_availables = iter(range(heights.shape[0]*heights.shape[1]))
        _, id = islice(id_availables, 2)  # Start with 1

        common_ids: Dict[int, Set[int]] = {}
        size_ids = defaultdict(int)

        def merge_ids(common_ids, id1, id2):
            shared_ids = common_ids[id1] | common_ids[id2]
            for id in shared_ids:
                common_ids[id] = shared_ids
            return common_ids

        ids = np.zeros(heights.shape, dtype=int)

        for i, j in np.ndindex(heights.shape):
            if heights[i, j] < 9:
                ids_up_left = list(
                    filter(lambda x: x != 0, up_and_left(ids, i, j)))
                if len(ids_up_left) == 0:
                    ids[i, j] = id
                    common_ids[id] = {id}
                    size_ids[id] += 1
                    id = next(id_availables)
                elif len(ids_up_left) == 1:
                    ids[i, j] = ids_up_left[0]
                    size_ids[ids_up_left[0]] += 1
                elif len(ids_up_left) == 2:
                    up, left = ids_up_left
                    merge_ids(common_ids, up, left)
                    ids[i, j] = up
                    size_ids[up] += 1
                else:
                    raise ValueError("Unexpected number of neighbours")

        def size_group(group: Set):
            return sum(size_ids[e] for e in group)
        top3 = islice(
            sorted((size_group(group) for group in set(frozenset(group) for _, group in common_ids.items())),
                   reverse=True),
            3)
        return reduce(operator.mul, top3), size_ids, ids, top3, common_ids


sol2()

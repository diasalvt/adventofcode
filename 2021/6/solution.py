import numpy as np
from numpy.typing import ArrayLike
from collections import Counter

def child(counter: int, days_left: int):
    if days_left == 0:
        return 1
    
    if counter == 0:
        return child(8, days_left - 1) + child(6, days_left - 1)
    else:
        return child(counter - 1, days_left - 1)
    
transition_matrix = np.array([
    [0, 1, 0, 0, 0, 0, 0, 0, 0], #0
    [0, 0, 1, 0, 0, 0, 0, 0, 0], #1
    [0, 0, 0, 1, 0, 0, 0, 0, 0], #2
    [0, 0, 0, 0, 1, 0, 0, 0, 0], #3
    [0, 0, 0, 0, 0, 1, 0, 0, 0], #4
    [0, 0, 0, 0, 0, 0, 1, 0, 0], #5
    [1, 0, 0, 0, 0, 0, 0, 1, 0], #6
    [0, 0, 0, 0, 0, 0, 0, 0, 1], #7
    [1, 0, 0, 0, 0, 0, 0, 0, 0] #8
])

def matrix_square(mat: ArrayLike) -> ArrayLike:
    return mat @ mat

def matrix_power(mat: ArrayLike, n:int) -> ArrayLike:
    if n == 1:
        return mat
    quotient, remainder = n // 2, n % 2

    if remainder:
        return matrix_square(matrix_power(mat, quotient)) @ mat
    else:
        return matrix_square(matrix_power(mat, quotient))
    
def sol1():
    with open("input6.txt") as f:
        internal_timers = map(int, next(f).split(','))
        days_left = 80

        result = sum(child(internal_timer, days_left) for internal_timer in internal_timers)
        print(result)

def sol2():
    with open("input6.txt") as f:
        internal_timers = list(map(int, next(f).split(',')))
        count_internal_timers = Counter(internal_timers)
        counts = np.array([0]*9)
        for key, value in count_internal_timers.items():
            counts[key] = value
        days_left = 256
    
        print(counts)
        transfo = matrix_power(transition_matrix, days_left) @ counts.transpose()
        print(sum(transfo))

sol1()
sol2()
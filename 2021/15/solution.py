from itertools import product
from collections import deque, defaultdict

test = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

with open("input15.txt") as f:
    lines = [row.strip() for row in f]

#lines = test.split('\n')


def neighbours_bottom_left(pos, grid):
    i, j = pos
    return {pos for pos in [(i, j + 1), (i + 1, j)] if pos in grid}


def sol1():
    max_cost = 9 * len(lines) * len(lines[0])
    grid = {(i, j): (int(val), 0 if i + j == 0 else max_cost)
            for i, line in enumerate(lines) for j, val in enumerate(line)}

    def shortest_path(grid):
        # start top left
        starting_pos = (0, 0)
        stack = [starting_pos]

        while stack:
            current_pos = stack.pop()
            current_val, current_cost = grid[current_pos]
            next_pos = neighbours_bottom_left(current_pos, grid)
            for pos in next_pos:
                pos_val, pos_cost = grid[pos]
                if pos_cost > (new_cost := current_cost + pos_val):
                    grid[pos] = pos_val, new_cost
                    stack.append(pos)

        print(max(grid.items(), key=lambda x: x[0])[1][1])


def sol2():
    _expansion = 5
    grid = {(i, j): int(val) for i, line in enumerate(lines)
            for j, val in enumerate(line)}
    max_i, max_j = max(grid)
    max_i += 1
    max_j += 1

    def neighbours(pos, max_i=max_i, max_j=max_j):
        i, j = pos
        return {(pos_i, pos_j) for pos_i, pos_j in [(i, j + 1), (i + 1, j), (i - 1, j), (i, j - 1)]
                if (0 <= pos_i < _expansion * max_i) and (0 <= pos_j < _expansion * max_j)}

    max_cost = (_expansion ** 2) * 9 * max_i * max_j

    grid_cost = defaultdict(lambda: max_cost)
    grid_cost[(0, 0)] = 0

    def get_val(grid, pos, max_i=max_i, max_j=max_j):
        i, j = pos
        quotient_i, remainder_i = i // max_i, i % max_i
        quotient_j, remainder_j = j // max_j, j % max_j

        val = (grid[(remainder_i, remainder_j)] + quotient_i + quotient_j) % 9
        if val:
            return val
        else:
            return 9

    def shortest_path(grid, grid_cost):
        # start top left
        starting_pos = (0, 0)
        stack = set([starting_pos])

        while stack:
            current_pos = stack.pop()
            current_val, current_cost = get_val(grid, current_pos), grid_cost[current_pos]
            next_pos = neighbours(current_pos)
            for pos in next_pos:
                pos_val, pos_cost = get_val(grid, pos), grid_cost[pos]
                if (new_cost := current_cost + pos_val) < pos_cost:
                    grid_cost[pos] = new_cost
                    stack.add(pos)

        print(grid_cost[(_expansion * max_i - 1, _expansion * max_j - 1)])

    shortest_path(grid, grid_cost)


sol2()

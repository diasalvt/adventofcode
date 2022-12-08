Grid = list[list[int]]


def parse_file(filename: str) -> Grid:
    with open(filename) as f:
        grid = [list(map(int, row)) for row in f.read().split()]

    return grid


test = parse_file('test.txt')
print(test)

def visibility(grid: Grid) -> set:

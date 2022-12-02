from statistics import median, mean

def sol1():
    with open("input7.txt") as f:
        values = list(map(int, next(f).split(',')))

        final_pos = median(values)
        total_fuel = sum((abs(value - final_pos) for value in values))
        print(total_fuel)

def loss(a, b):
    return abs(a-b)*(abs(a-b)+1)/2

def sol2():
    with open("input7.txt") as f:
        values = list(map(int, next(f).split(',')))

        mean_pos = int(mean(values))
        total_fuel_by_pos = sum((loss(value, mean_pos) for value in values))
        print(total_fuel_by_pos)

sol1()
sol2()
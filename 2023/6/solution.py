from math import prod


def load(filename: str) -> list[tuple[int, int]]:
    return list(zip(*(map(int, line.split()[1:]) for line in open(filename))))


races = load('input.txt')

print(
    prod(
        sum(i*(time - i) > dist for i in range(time + 1))
        for time, dist in races
    )
)

times, dists = zip(*races)
time = int(''.join(str(t) for t in times))
dist = int(''.join(str(d) for d in dists))

print(
    sum(i*(time - i) > dist for i in range(time + 1))
)

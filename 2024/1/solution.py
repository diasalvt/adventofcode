from collections import Counter


def read(filename: str) -> tuple[list, list]:
    with open(filename) as f:
        list_a, list_b = zip(
            *[map(int, line.split()) for line in f.read().splitlines()]
        )
    return list_a, list_b


a, b = read('input.txt')
sorted_a, sorted_b = map(sorted, read('input.txt'))
print(
    sum(abs(a_i - b_i) for a_i, b_i in zip(sorted_a, sorted_b))
)

c_b = Counter(b)
print(
    sum(c_b[a_i] * a_i for a_i in a)
)

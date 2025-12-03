def load(filename: str) -> list[tuple[int]]:
    with open(filename) as f:
        return [
            tuple(map(int, r))
            for r in f.read().splitlines()
        ]


def max_joltage(data: tuple[int], size: int = 2) -> tuple[int, int]:
    rest = size - 1

    if rest == 0:
        return max(data)

    i = min(i for i, v in enumerate(data[:-rest]) if v == max(data[:-rest]))

    return data[i] * 10**rest + max_joltage(data[i + 1:], rest)


print(
    sum(
        max_joltage(d)
        for d in load('input.txt')
    )
)


print(
    sum(
        max_joltage(d, size=12)
        for d in load('input.txt')
    )
)

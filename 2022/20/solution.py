def parse_file(filename: str) -> list[int]:
    with open(filename) as f:
        return list(map(int, f.read().splitlines()))


test = parse_file('test.txt')
print(test)


def move(l: list, current_idx: int, movement: int) -> list:
    future_idx = (current_idx + movement) % (len(l) - 1)

    val = l.pop(current_idx)
    l.insert(future_idx, val)

    return l, future_idx


def get(l: list, idx: int) -> int:
    return l[idx % len(l)]


def test_move():
    data = [1, 2, 3, 4, 5]
    assert move(data, 2, -2) == ([3, 1, 2, 4, 5], 0)

    data = [1, 2, 3, 4, 5]
    assert move(data, 0, 2)  == ([2, 3, 1, 4, 5], 2)

    data = [1, 2, 3, 4, 5]
    assert move(data, 4, 1)  == ([1, 5, 2, 3, 4], 1)

    data = [1, 2, 3, 4, 5]
    assert move(data, 0, -1) == ([2, 3, 4, 1, 5], 3)

    data = [1, 2, 3, 4, 5]
    assert move(data, 4, 2)  == ([1, 2, 5, 3, 4], 2)

    data = [1, 2, 3, 4, 5]
    assert move(data, 4, 3)  == ([1, 2, 3, 5, 4], 3)

    data = [1, 2, 3, 4, 5]
    assert move(data, 4, 4)  == ([5, 1, 2, 3, 4], 0)

    data = [1, 2, 3, 4, 5]
    assert move(data, 4, 5)  == ([1, 5, 2, 3, 4], 1)

    data = [1, 2, 3, 4, 5]
    assert move(data, 4, -4) == ([5, 1, 2, 3, 4], 0)

    data = [1, 2, 3, 4, 5]
    assert move(data, 4, -8) == ([5, 1, 2, 3, 4], 0)


def part_1(filename: str) -> int:
    data = parse_file(filename)
    positions = list(range(len(data)))
    for i, shift in enumerate(data[:]):
        previous_pos = positions[i]
        data, new_pos = move(data, previous_pos, shift)
        a, b = sorted([previous_pos, new_pos])
        # Shift indexes of positions between
        for j, p in enumerate(positions):
            if a <= p <= b:
                positions[j] += -1 if previous_pos < new_pos else 1
        positions[i] = new_pos

    idx_0 = data.index(0)

    return (
        get(data, idx_0 + 1000) +
        get(data, idx_0 + 2000) +
        get(data, idx_0 + 3000)
    )


# print(part_1('test.txt'))
print(part_1('input.txt'))


def part_2(filename: str) -> int:
    key = 811589153

    data = list(map(lambda x: x * key, parse_file(filename)))
    positions = list(range(len(data)))
    original_data = data[:]
    for _ in range(10):
        for i, shift in enumerate(original_data):
            previous_pos = positions[i]
            data, new_pos = move(data, previous_pos, shift)
            a, b = sorted([previous_pos, new_pos])
            for j, p in enumerate(positions):
                if a <= p <= b:
                    positions[j] += -1 if previous_pos < new_pos else 1
            positions[i] = new_pos
    idx_0 = data.index(0)

    return (
        get(data, idx_0 + 1000) +
        get(data, idx_0 + 2000) +
        get(data, idx_0 + 3000)
    )


# print(part_2('test.txt'))
print(part_2('input.txt'))

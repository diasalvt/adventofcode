from itertools import pairwise, starmap


def load(filename: str) -> list[list[int]]:
    with open(filename) as f:
        return [
            list(map(int, line.split()))
            for line in f
        ]


puzzle = load('input.txt')
puzzle_test = load('test.txt')


def pred_seq(seq: list[int]) -> int:
    if not any(seq):
        return 0
    return seq[-1] + pred_seq(list(starmap(lambda x, y: y - x, pairwise(seq))))


def test_pred_seq():
    assert sum(pred_seq(line) for line in puzzle_test) == 114


print(sum(pred_seq(line) for line in puzzle))
print(sum(pred_seq(line[::-1]) for line in puzzle))

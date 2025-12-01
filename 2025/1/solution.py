from itertools import accumulate, pairwise, starmap
from operator import add


def load(filename: str) -> list[int]:
    with open(filename) as f:
        return [
            int(r[1:]) * (1 if r[0] == 'R' else -1)
            for r in f.read().splitlines()
        ]


input_data = load('input.txt')

acc_shifts = list(accumulate([50] + input_data, func=add))

result_part_1 = (
    sum(
        (x % 100) == 0
        for x in acc_shifts
    )
)

# count multiples of 100 between shifts
# We are manipulating ranges [x, y], [y, z], so we have double counting
# if y is 0. We correct by removing result from part 1.
# But if the last element was 0 in such case there is no double counting.
result_part_2 = (
    sum(
        starmap(
            lambda x, y: sum((x % 100) == 0 for x in range(x, y + 1)),
            map(sorted, pairwise(acc_shifts))
        )
    )
) - result_part_1 + (0 if acc_shifts[-1] % 100 else 1)

from typing import TypeAlias, Iterable
import re
from collections import defaultdict
from itertools import pairwise, permutations, chain, islice


Person: TypeAlias = str
AffinityMap = defaultdict[Person, dict[Person, int]]

_LINE_REGEX = re.compile(
    r'(?P<person_1>\w+) would (?P<sign>gain|lose) (?P<quantity>\d+)'
    r' happiness units by sitting next to (?P<person_2>\w+).'
    '\n'
)


def get_data(filename: str) -> AffinityMap:
    affinity_map: AffinityMap = defaultdict(dict)
    with open(filename) as f:
        for line in f.readlines():
            match = _LINE_REGEX.fullmatch(line)
            assert match is not None
            p_1, p_2 = match['person_1'], match['person_2']
            cost = int(match['quantity']) * (-1 if match['sign'] == 'lose' else 1)

            affinity_map[p_1][p_2] = cost

    return affinity_map


print(f'{get_data("test.txt")}')


def eval_arrangement_cost(arrangement: Iterable[Person], affinity_map: AffinityMap) -> int:
    total_cost = 0

    arrangement = list(arrangement)
    for p_1, p_2 in pairwise(chain(arrangement, islice(arrangement, 1))):
        total_cost += (
            affinity_map[p_1][p_2] +
            affinity_map[p_2][p_1]
        )

    return total_cost


def test_eval_arrangement_cost():
    assert eval_arrangement_cost(
        ['Alice', 'Bob', 'Carol', 'David'], get_data('test.txt')
    ) == 330


def find_best_arrangement(affinity_map: AffinityMap) -> Iterable[Person]:
    first_person, *others = affinity_map.keys()

    def prepend_to_each(element, iterables: Iterable):
        for iterable in iterables:
            yield list(chain([element], iterable))

    return max(
        map(
            lambda x: eval_arrangement_cost(x, affinity_map),
            prepend_to_each(first_person, permutations(others))
        )
    )


def modify_affinity(affinity_map: AffinityMap) -> AffinityMap:
    result = defaultdict(dict)
    for k, v in affinity_map.items():
        result[k] = v
        result[k]['Me'] = 0
    for p in affinity_map.keys():
        result['Me'][p] = 0
    return result


print(find_best_arrangement(get_data('input.txt')))
print(find_best_arrangement(modify_affinity(get_data('input.txt'))))
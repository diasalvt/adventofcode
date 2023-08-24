# Shortest path problem
import re
from typing import Final
from collections import defaultdict
import heapq

City = str
Graph = defaultdict[City, list[tuple[City, int]]]


def get_data(filename: str) -> Graph:
    pattern: Final[re.Patter[str]] = re.compile(r'(\w+) to (\w+) = (\d+)')

    graph = defaultdict(list)
    cities = set()
    with open(filename) as f:
        for line in f.read().splitlines():
            city_a, city_b, cost = pattern.fullmatch(line).groups()
            graph[city_a] += [(city_b, int(cost))]
            graph[city_b] += [(city_a, int(cost))]
            cities |= {city_a, city_b}

    graph['_Start'] = [(city, 0) for city in cities]
    return graph


# print(get_data('test.txt'))


def shortest_path(graph: Graph) -> int:
    current_states: list[tuple[int, City, set[City]]] = []
    heapq.heappush(current_states, (0, '_Start', {'_Start'}))

    cities = set(graph)

    while True:
        state = heapq.heappop(current_states)
        actual_cost, city, seen_cities = state
        if seen_cities == cities:
            return actual_cost

        for next_city, cost in graph[city]:
            if not next_city in seen_cities:
                heapq.heappush(current_states, (actual_cost + cost, next_city, seen_cities | {next_city}))


def test_shortest_path():
    assert shortest_path(get_data('test.txt')) == 605


print(shortest_path(get_data('input.txt')))


def part_2(filename: str) -> int:
    graph = get_data(filename)
    new_graph = {k: [(city, -cost) for city, cost in v] for k, v in graph.items()}

    return -shortest_path(new_graph)


def test_part_2():
    assert part_2('test.txt') == 682


print(part_2('input.txt'))

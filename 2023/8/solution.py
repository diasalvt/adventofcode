from typing import Self
from dataclasses import dataclass
import re
from itertools import cycle
from collections import defaultdict
from math import prod, gcd


@dataclass
class Node:
    name: str
    left: str
    right: str

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls(*re.findall(r'\w{3}', s))


Instructions = str
Graph = dict[str, Node]


def load(filename: str) -> tuple[Instructions, Graph]:
    lines = open(filename).read().splitlines()
    instructions = lines[0]

    graph = {}
    for line in lines[2:]:
        n = Node.from_str(line)
        graph[n.name] = n

    return (
        instructions,
        graph
    )


instructions, graph = load('input.txt')
instructions_test, graph_test = load('test.txt')
instructions_test2, graph_test2 = load('test2.txt')


def run(instructions: Instructions, graph: Graph) -> int:
    curr = 'AAA'
    end = 'ZZZ'

    for i, instruction in enumerate(cycle(instructions), start=1):
        match instruction:
            case 'L':
                curr = graph[curr].left
            case 'R':
                curr = graph[curr].right
            case _:
                raise ValueError(
                    f'{instruction=} is not a valid direction, step {i}'
                )
        if curr == end:
            return i


def test_run():
    assert run(instructions_test, graph_test) == 6


print(run(instructions, graph))


def lcm(numbers: list[int]) -> int:
    _gcd = gcd(*numbers)
    return prod(n // _gcd for n in numbers) * _gcd


def run_2(instructions: Instructions, graph: Graph) -> int:
    ghosts = [node_name for node_name in graph if node_name.endswith('A')]
    ending_positions = defaultdict(list)
    cycle_length = {}

    for node_name in ghosts:
        curr = node_name
        seen_positions = {}
        for i, (pos_inst, inst) in enumerate(cycle(enumerate(instructions)), start=1):
            match inst:
                case 'L':
                    curr = graph[curr].left
                case 'R':
                    curr = graph[curr].right
                case _:
                    raise ValueError(
                        f'{inst=} is not a valid direction, step {i}'
                    )

            if (pos_inst, curr) in seen_positions:
                cycle_length[node_name] = i - seen_positions[(pos_inst, curr)]
                break
            seen_positions[(pos_inst, curr)] = i

            if curr.endswith('Z'):
                ending_positions[node_name].append((i, curr))
    return lcm([pos[0][0] for pos in ending_positions.values()])


# print(run_2(instructions_test2, graph_test2))
print(run_2(instructions, graph))

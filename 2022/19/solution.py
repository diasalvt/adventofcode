from dataclasses import dataclass
from enum import Enum
from collections import Counter
from typing import Self, Final, NamedTuple
import re
from math import ceil


class Rock(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4


LINE: Final[re.Pattern[str]] = re.compile(
    r'Blueprint \d+: Each ore robot costs (?P<ore_robot>\d+) ore. '
    r'Each clay robot costs (?P<clay_robot>\d+) ore. '
    r'Each obsidian robot costs (?P<obsidian_robot_ore>\d+) ore and (?P<obsidian_robot_clay>\d+) clay. '
    r'Each geode robot costs (?P<geode_robot_ore>\d+) ore and (?P<geode_robot_obsidian>\d+) obsidian.'
)


@dataclass
class Blueprint:
    recipes: dict[Rock, Counter[Rock]]

    @classmethod
    def from_str(cls, s: str) -> Self:
        match = LINE.match(s)
        assert match is not None
        recipes = {
            Rock.ORE: Counter({Rock.ORE: int(match['ore_robot'])}),
            Rock.CLAY: Counter({Rock.ORE: int(match['clay_robot'])}),
            Rock.OBSIDIAN: Counter({
                Rock.ORE: int(match['obsidian_robot_ore']),
                Rock.CLAY: int(match['obsidian_robot_clay'])
            }),
            Rock.GEODE: Counter({
                Rock.ORE: int(match['geode_robot_ore']),
                Rock.OBSIDIAN: int(match['geode_robot_obsidian'])
            })
        }
        return cls(recipes)


def parse_file(filename: str) -> list[Blueprint]:
    with open(filename) as f:
        return [Blueprint.from_str(line) for line in f.read().splitlines()]


test = parse_file('test.txt')
blueprints = parse_file('input.txt')
# print(test)


class State(NamedTuple):
    robots: Counter[Rock]
    rocks: Counter[Rock]
    time_left: int


def compute_next_states(
    state: State, blueprint: Blueprint, max_state: State
) -> list[State]:
    next = []
    robots, rocks, time_left = state
    if time_left == 0:
        return next

    if (rocks[Rock.GEODE]*time_left + (time_left * (time_left + 1) / 2)) < max_state.rocks[Rock.GEODE]:
        return next

    for robot in Rock:
        dependencies = blueprint.recipes[robot]

        # If one dependency is not available
        if any(state.robots[robot] == 0 for robot in dependencies):
            continue

        time_needed = max([
            ceil((count - rocks[rock_needed]) / state.robots[rock_needed])
            for rock_needed, count in dependencies.items()
        ]) + 1
        time_needed = max(1, time_needed)

        if time_needed <= time_left:
            next.append(State(
                robots + Counter([robot]),
                (
                    rocks +
                    Counter({rock: time_needed*c for rock, c in robots.items()}) -
                    dependencies
                ),
                time_left - time_needed
            ))

    if (not next):
        return [State(
            robots,
            rocks + Counter({rock: time_left*c for rock, c in robots.items()}),
            0
        )]

    return next


def search(initial_state: State, blueprint: Blueprint) -> State:
    next_states = [initial_state]
    max_state = initial_state
    while next_states:
        state = next_states.pop()
        next_states += compute_next_states(state, blueprint, max_state)
        if state.rocks[Rock.GEODE] > max_state.rocks[Rock.GEODE]:
            max_state = state
    return max_state


initial_state = State(Counter([Rock.ORE]), Counter(), 24)
# print(compute_next_states(initial_state, test[0]))
# print(search(initial_state, test[0]))
# print(search(initial_state, test[1]))

def part_1(filename: str) -> int:
    blueprints = parse_file(filename)
    res = 0
    for i, blueprint in enumerate(blueprints):
        initial_state = State(Counter([Rock.ORE]), Counter(), 24)
        max_geode = search(initial_state, blueprint).rocks[Rock.GEODE]
        print(i, max_geode)
        res += (i + 1) * max_geode
    return res


print(part_1('input.txt'))

from dataclasses import dataclass
from enum import Enum
from collections import Counter
from typing import Self, Final, NamedTuple
import re


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
    robots: dict[Rock, Counter[Rock]]

    @classmethod
    def from_str(cls, s: str) -> Self:
        print(s)
        match = LINE.match(s)
        assert match is not None
        robots = {
            Rock.ORE: Counter({Rock.ORE: match['ore_robot']}),
            Rock.CLAY: Counter({Rock.ORE: match['clay_robot']}),
            Rock.OBSIDIAN: Counter({
                Rock.ORE: match['obsidian_robot_ore'],
                Rock.CLAY: match['obsidian_robot_clay']
            }),
            Rock.GEODE: Counter({
                Rock.ORE: match['geode_robot_ore'],
                Rock.OBSIDIAN: match['geode_robot_obsidian']
            })
        }
        return cls(robots)

    def __getattribute__(self, name: str) -> Counter[Rock]:
        return self.robots[name]

def parse_file(filename: str) -> list[Blueprint]:
    with open(filename) as f:
        return [Blueprint.from_str(line) for line in f.read().splitlines()]


print(parse_file('test.txt'))


class State(NamedTuple):
    robots: Counter[Rock]
    rocks: Counter[Rock]
    time_left: int


def next_states(state: State, blueprint: Blueprint) -> list[State]:
    for robot in Rock:
        dependencies = blueprint.robot

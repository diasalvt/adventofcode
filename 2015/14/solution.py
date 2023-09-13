import re
from dataclasses import dataclass
from typing import TypeAlias, Self

Km_Second: TypeAlias = int
Km: TypeAlias = int
Second: TypeAlias = int


_LINE_REGEX = re.compile(
    r'(?P<name>\w+) can fly (?P<speed>\d+) km/s '
    r'for (?P<duration>\d+) seconds, '
    r'but then must rest for (?P<rest>\d+) seconds.'
)


@dataclass
class Spec:
    name: str
    speed: Km_Second
    duration: Second
    rest: Second

    @classmethod
    def from_str(cls, line: str) -> Self:
        match = _LINE_REGEX.fullmatch(line)
        assert match is not None

        name, speed = match.group('name'), int(match.group('speed'))
        duration, rest = int(match.group('duration')), int(match.group('rest'))
        return cls(name, speed, duration, rest)


def get_specs(filename: str) -> list[Spec]:
    with open(filename) as f:
        return [Spec.from_str(line) for line in f.read().splitlines()]


print(test_specs := get_specs('test.txt'))


def km_traveled(spec: Spec, time: Second) -> Km:
    cycle_duration = spec.duration + spec.rest
    quotient, rest = time // cycle_duration, time % cycle_duration

    return (quotient * spec.duration + min(spec.duration, rest)) * spec.speed


print(
    *[km_traveled(spec, 1000) for spec in test_specs],
    sep='\n'
)


def best_spec(specs: list[Spec], time: Second) -> Km:
    return max(
        km_traveled(spec, time) for spec in specs
    )


print(
    f'Distance of the winning reindeer: '
    f'{best_spec(get_specs("test.txt"), 1000)}'
)
print(
    f'Distance of the winning reindeer: '
    f'{best_spec(get_specs("input.txt"), 2503)}'
)


def part_2(specs: list[Spec], time: Second) -> int:
    points = [0] * len(specs)

    for t in range(1, time + 1):
        distances = [km_traveled(spec, t) for spec in specs]
        max_distance = max(distances)
        points = [p + 1 if d == max_distance else p for p, d in zip(points, distances)]

    return max(points)


print(part_2(get_specs('input.txt'), 2503))

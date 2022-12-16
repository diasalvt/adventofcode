import re
from itertools import chain

Valve = str
ValveSystem = tuple[dict[Valve, int], dict[Valve, list[Valve]]]


def parse_file(filename: str) -> ValveSystem:
    with open(filename) as f:
        rate_valves = [
            (re.findall(r'\d+', row)[0], re.findall(r'[A-Z][A-Z]', row))
            for row in f.read().splitlines()
        ]
        print(rate_valves)

        return (
            {valve: int(r) for r, (valve, *_) in rate_valves},
            {valve: connected_valves for _,
                (valve, *connected_valves) in rate_valves}
        )


test = parse_file('test.txt')
starting_valve = 'AA'
duration = 30


# Recursive way
def set_zero(valve_system: ValveSystem, valve) -> ValveSystem:
    flow_rate, connected_values = valve_system
    return (
        {**flow_rate, valve: 0},
        connected_values
    )


def best_sequence(
    current_valve: Valve, time_left: int, valve_system: ValveSystem
) -> int:
    flow_rate, connected_valves = valve_system

    if time_left == 0:
        return 0
    else:
        move_sequence = max([
            best_sequence(next_valve, time_left - 1, valve_system)
            for next_valve in connected_valves[current_valve]
        ])

        if flow_rate[current_valve] > 0:
            open_valve_sequence = (
                (flow_rate[current_valve] * (time_left - 1)) +
                best_sequence(current_valve, time_left - 1,
                              set_zero(valve_system, current_valve))
            )
            return max(open_valve_sequence, move_sequence)
        else:
            return move_sequence


# print(best_sequence('AA', 30, test))
def upper_bound(
    valve: Valve, time_left: int, valve_system: ValveSystem
) -> int:
    flow_rate, connected_valves = valve_system
    next_valves = {valve}
    max_pressure_release = 0
    for i in reversed(range(1, time_left)):
        max_pressure_release += max(flow_rate[v] for v in next_valves) * i
        next_valves = set(chain.from_iterable(
            connected_valves[v] for v in next_valves
        ))

    return max_pressure_release


def bfs(start: Valve, duration: int, valve_system: ValveSystem) -> int:
    next_valves = [(start, 0, set())]
    current_best = 0
    flow_rate, connected_valves = valve_system

    for i in reversed(range(0, duration)):
        _future_next_valves = []
        print(i, len(next_valves))
        for valve, pressure_released, opened_valves in next_valves:
            #  Open valve
            if (flow_rate[valve] > 0) and (valve not in opened_valves):
                _future_next_valves += [(
                    valve,
                    pressure_released + flow_rate[valve]*i,
                    opened_valves | {valve}
                )]
            #  Skip release
            else:
                _future_next_valves += [
                    (v, pressure_released, opened_valves)
                    for v in connected_valves[valve]
                    if (pressure_released + upper_bound(v, i, valve_system)) > current_best
                ]
        if len(_future_next_valves) == 0:
            return max(next_valves, key=lambda x: x[1])
        next_valves = _future_next_valves
        current_best = max(next_valves, key=lambda x: x[1])[1]

    return next_valves


print(bfs('AA', 30, test))

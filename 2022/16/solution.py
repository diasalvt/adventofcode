import re
from collections import defaultdict
from itertools import chain, product
from typing import Iterable

Valve = str
ValveSystem = tuple[dict[Valve, int], dict[Valve, list[Valve]]]


def parse_file(filename: str) -> ValveSystem:
    with open(filename) as f:
        rate_valves = [
            (re.findall(r'\d+', row)[0], re.findall(r'[A-Z][A-Z]', row))
            for row in f.read().splitlines()
        ]

        return (
            {valve: int(r) for r, (valve, *_) in rate_valves},
            {valve: connected_valves for _,
                (valve, *connected_valves) in rate_valves}
        )


test = parse_file('test.txt')


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


print(best_sequence('AA', 10, test))


def upper_bound(
    valve: Valve, time_left: int, valve_system: ValveSystem
) -> int:
    flow_rate, connected_valves = valve_system
    next_valves = {valve}
    max_pressure_release = 0
    for i in reversed(range(time_left)):
        max_pressure_release += max(flow_rate[v] for v in next_valves) * i
        next_valves = set(chain.from_iterable(
            connected_valves[v] for v in next_valves
        ))

    return max_pressure_release


def bfs(
    start: Valve, duration: int, valve_system: ValveSystem
) -> int:
    next_valves = {(start, 0, frozenset())}
    current_best = 0
    flow_rate, connected_valves = valve_system

    for i in reversed(range(duration)):
        _future_next_valves = set()
        print(i, len(next_valves))
        for valve, pressure_released, opened_valves in next_valves:
            #  Open valve
            if (flow_rate[valve] > 0) and (valve not in opened_valves):
                _future_next_valves |= {(
                    valve,
                    pressure_released + flow_rate[valve]*i,
                    opened_valves | {valve},
                )}
            #  Skip release
            _future_next_valves |= set((
                (v, pressure_released, opened_valves)
                for v in connected_valves[valve]
                if (pressure_released + upper_bound(v, i, valve_system)) > current_best
            ))
        if len(_future_next_valves) > 0:
            next_valves = _future_next_valves
            current_best = max(next_valves, key=lambda x: x[1])[1]
        else:
            return next_valves

    return next_valves


print(max(bfs('AA', 10, test), key=lambda x: x[1]))
# print(max(bfs('AA', 30, parse_file('input.txt')), key=lambda x: x[1]))
State = tuple[tuple[Valve, ...], int, frozenset]


def product_player_states(player_states: Iterable, current_state: State):
    valves, pressure_released, opened_valves = current_state

    next_states = set()
    for states in product(*player_states):
        new_opened_valves = list(chain.from_iterable(
            state[2] - opened_valves
            for state in states
        ))
        unique_opened_valves = frozenset(new_opened_valves)
        # we dont open twice the same valve
        if len(new_opened_valves) == len(unique_opened_valves):
            next_states |= {(
                tuple(state[0] for state in states),
                pressure_released + sum(state[1] for state in states),
                opened_valves | unique_opened_valves
            )}
    return next_states


def bfs2(
    start: Valve, duration: int, valve_system: ValveSystem, nb_player: int = 1
) -> int:

    def upper_bound(
        state: State, time_left: int, valve_system: ValveSystem
    ) -> int:
        flow_rate, connected_valves = valve_system
        next_valves = [{valve} for valve in state[0]]
        max_pressure_release = 0
        for t in reversed(range(1, time_left + 1)):
            for i, valves in enumerate(next_valves):
                max_pressure_release += t * max(
                    (flow_rate[v] for v in valves),
                    default=0
                )
                next_valves[i] = set(chain.from_iterable(
                    connected_valves[v] for v in valves
                ))

        return max_pressure_release

    next_states = {((start,)*nb_player, 0, frozenset())}
    current_best = 0
    flow_rate, connected_valves = valve_system

    for i in reversed(range(1, duration)):
        _future_next_states = set()
        print(i, len(next_states))
        for valves, pressure_released, opened_valves in next_states:
            player_states = [set() for _ in range(nb_player)]
            for player in range(nb_player):
                valve = valves[player]
                #  Open valve
                if (flow_rate[valve] > 0) and (valve not in opened_valves):
                    player_states[player] |= {(
                        valve,
                        flow_rate[valve]*i,
                        opened_valves | {valve},
                    )}
                #  Skip release
                player_states[player] |= set(
                    (v, 0, opened_valves)
                    for v in connected_valves[valve]
                )

            _future_next_states |= product_player_states(
                player_states,
                (valves, pressure_released, opened_valves)
            )

        _future_next_states = set(filter(
            lambda x: (x[1] + upper_bound(x, i, valve_system)) > current_best,
            _future_next_states
        ))
        # Keep max for a specific current valves and opened valves state
        max_states = defaultdict(int)
        for valves, pressure_released, opened_valves in _future_next_states:
            max_states[(valves, opened_valves)] = max(
                max_states[(valves, opened_valves)], pressure_released
            )

        _future_next_states = {
            (valves, pressure_released, opened_valves)
            for (valves, opened_valves), pressure_released in max_states.items()
        }

        if len(_future_next_states) > 0:
            next_states = _future_next_states
            current_best = max(next_states, key=lambda x: x[1])[1]
        else:
            return next_states

    return next_states


# print(max(bfs2('AA', 26, parse_file('test.txt'), nb_player=2), key=lambda x: x[1]))
print(max(bfs2('AA', 26, parse_file('input.txt'), nb_player=2), key=lambda x: x[1]))

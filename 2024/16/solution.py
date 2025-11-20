from functools import reduce
from math import inf

Pos = complex
Player = tuple[Pos, complex]
Terrain = dict[Pos, str]


def load(filename: str) -> Terrain:
    with open(filename) as f:
        return {
            x + y * 1j: c
            for y, row in enumerate(f.read().splitlines())
            for x, c in enumerate(row)
        }


def add_wall(terrain: Terrain, pos: Pos) -> Terrain:
    return {
        p: t if p != pos else '▨'
        for p, t in terrain.items()
    }


def is_fork(pos: Pos, terrain: Terrain) -> bool:
    return (
        sum(terrain[pos + d] in {'.', 'E'} for d in {1, -1, 1j, -1j}) >
        1
    )


def display(terrain: Terrain) -> None:
    x, y = 0, 0
    text = ''
    while len(terrain) > 0:
        if (p := (x + y * 1j)) in terrain:
            text += terrain[x + y * 1j]
            terrain = {k: v for k, v in terrain.items() if k != p}
            x += 1
        else:
            text += '\n'
            x = 0
            y += 1
    print(text)


def forward(
    player: Player, terrain: Terrain
) -> tuple[bool, Player, Terrain]:
    pos, direction = player
    for d in {1, -1, 1j, -1j} - {-direction}:
        if terrain[pos + d] in {'.', 'E'}:
            return True, (pos + d, d), add_wall(terrain, pos)
    return False, (pos, d), terrain


def longest_path(player: Player, terrain: Terrain) -> int:
    path_length = 0
    while not is_fork(player[0], terrain):
        if terrain[player[0]] == 'E':
            return path_length
        can_move, new_player, terrain = forward(player, terrain)
        path_length += 1 if player[1] == new_player[1] else 1001
        player = new_player
        if not can_move:
            return 100_000

    pos, direction = player
    new_terrain = add_wall(terrain, pos)
    return 1 + path_length + max(
        (
            (
                longest_path((pos + d, d), new_terrain) +
                (0 if direction == d else 1000)
            )
            for d in {1, -1, 1j, -1j}
            if new_terrain[pos + d] in {'.', 'E'}
        ),
        default=100_000
    )


Node = Player
Graph = dict[Node, list[tuple[Node, int]]]


def make_graph(terrain: Terrain) -> Graph:
    def neighbours(
        player: Player, terrain: Terrain
    ) -> list[tuple[Player, int]]:
        position, direction = player
        return [
            ((position + d, d), 1 if d == direction else 1001)
            for d in {1, -1, 1j, -1j} - {-direction}
            if terrain[position + d] in {'.', 'E'}
        ]

    start = {t: p for p, t in terrain.items()}['S']
    to_explore = [(start, 1)]
    graph = {}

    while to_explore:
        next_node = to_explore.pop()
        if next_node not in graph.keys():
            graph[next_node] = neighbours(next_node, terrain)
            to_explore.extend([p for p, c in graph[next_node]])

    return graph


def dijkstra(graph: Graph, start: Node):
    # Initialize
    dijkstra_struct = {
        node: (inf, []) if node != start else (0, [])
        for node in graph
    }

    to_solve = [(0, start)]

    while to_solve:
        to_solve = sorted(to_solve, key=lambda x: x[0], reverse=True)
        cost, node = to_solve.pop()
        for n, c in graph[node]:
            cost_n = cost + c
            current_cost, current_predecessors = dijkstra_struct[n]
            if current_cost > cost_n:
                dijkstra_struct[n] = (cost_n, [node])
                to_solve.append((cost_n, n))
            elif current_cost == cost_n:
                dijkstra_struct[n] = (cost_n, current_predecessors + [node])

    return dijkstra_struct


terrain = load('input.txt')
start = {t: p for p, t in terrain.items()}['S']
end = {t: p for p, t in terrain.items()}['E']
graph = make_graph(terrain)
print(
    min(
        info
        for (p, d), info in dijkstra(graph, (start, 1)).items()
        if p == end
    )
)

_, end_node = min(
    (cost, (p, d))
    for (p, d), (cost, _) in dijkstra(graph, (start, 1)).items()
    if p == end
)


def get_predecessors(player: Player, dijkstra_struct: dict) -> set[Pos]:
    return {player} | reduce(
        lambda x, y: x | y,
        map(
            lambda x: get_predecessors(x, dijkstra_struct),
            dijkstra_struct[player][1]
        ),
        set()
    )


pred = {
    pos
    for pos, d in get_predecessors(end_node, dijkstra(graph, (start, 1)))
}

print(len(pred))

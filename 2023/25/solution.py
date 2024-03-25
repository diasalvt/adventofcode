from collections import defaultdict, Counter
import re
from itertools import chain, pairwise
import networkx as nx
import matplotlib.pyplot as plt
import random

Graph = defaultdict[str, set[str]]


def load(filename: str) -> Graph:
    d = defaultdict(set)
    with open(filename) as f:
        for row in f:
            main_node, *connected_nodes = re.findall(r'\w+', row)
            for n in connected_nodes:
                d[main_node].add(n)
                d[n].add(main_node)
    return d


test = load('test.txt')
graph = load('input.txt')
nx.draw(nx.Graph(graph), with_labels=True)
plt.savefig('graph.png')


def count_connected(graph: Graph, node: str) -> int:
    seen = set()
    to_visit = {node}
    while to_visit:
        seen |= to_visit
        to_visit = set(chain.from_iterable(graph[v] for v in to_visit)) - seen
    return len(seen)


def cut_graph(graph: Graph, edge: tuple[str, str]) -> graph:
    node_a, node_b = edge

    def to_del(node: str) -> set[str]:
        if node == node_a:
            return {node_b}
        elif node == node_b:
            return {node_a}
        else:
            return set()

    return {
        k: v - to_del(k)
        for k, v in graph.items()
    }


graph_sol = cut_graph(graph, ('zsp', 'fhv'))
graph_sol = cut_graph(graph_sol, ('hcd', 'cnr'))
graph_sol = cut_graph(graph_sol, ('fqr', 'bqp'))
print(
    count_connected(graph_sol, 'zsp') * count_connected(graph_sol, 'fhv')
)


def random_walk(graph: Graph, node: str) -> int:
    path = [node]
    while True:
        try:
            node = random.choice([v for v in graph[node] if v not in path])
            path.append(node)
        except IndexError:
            return path


nodes = graph.keys()

random.seed(0)
c = Counter()
paths_many_nodes = filter(
    lambda x: len(x) > (0.3*len(nodes)),
    (
        random_walk(graph, n)
        for n in nodes
    )
)
c.update(
    map(
        lambda x: tuple(sorted(x)),
        chain.from_iterable(map(pairwise, paths_many_nodes))
    )
)

candidates, _ = zip(*sorted(c.items(), key=lambda x: x[1], reverse=True)[:10])
edge1, edge2, edge3 = candidates[:3]

graph_sol = cut_graph(graph, edge1)
graph_sol = cut_graph(graph_sol, edge2)
graph_sol = cut_graph(graph_sol, edge3)

print(
    count_connected(graph_sol, edge1[0]) * count_connected(graph_sol, edge1[1])
)

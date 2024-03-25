from collections import defaultdict, Counter
import re
from itertools import chain
import networkx as nx
import matplotlib.pyplot as plt

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
print(*test.items(), sep='\n')
print(Counter(chain.from_iterable(test.values())))
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
    graph[node_a].discard(node_b)
    graph[node_b].discard(node_a)
    return graph


graph = cut_graph(graph, ('zsp', 'fhv'))
graph = cut_graph(graph, ('hcd', 'cnr'))
graph = cut_graph(graph, ('fqr', 'bqp'))
print(
    count_connected(graph, 'zsp') * count_connected(graph, 'fhv')
)

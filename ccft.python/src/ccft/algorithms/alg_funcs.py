import networkx as nx


def __networkx_iterator_succ__(G: nx.DiGraph, node):
    return G.successors(node)


def __networkx_iterator_pred__(G: nx.DiGraph, node):
    return G.predecessors(node)


def __networkx_iterator_neighbors__(G: nx.DiGraph, node):
    return list(G.predecessors(node)) + list(G.successors(node))

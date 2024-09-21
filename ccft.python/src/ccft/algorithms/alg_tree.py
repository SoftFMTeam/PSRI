import networkx as nx

from ccft.algorithms.alg_funcs import __networkx_iterator_pred__, __networkx_iterator_succ__


def networkx_tree(G: nx.DiGraph, root, succ_dir=True, max_depth=-1):
    T = nx.DiGraph()

    queue = [root]
    visited = {root}

    depth = 0

    if succ_dir:
        iterator = __networkx_iterator_succ__
    else:
        iterator = __networkx_iterator_pred__

    if max_depth > 0:
        while queue and max_depth > depth:
            queue = __networkx_next_nodes__(G, T, queue, visited, iterator)
            depth += 1
    else:
        while queue:
            queue = __networkx_next_nodes__(G, T, queue, visited, iterator)

    return T


def __networkx_next_nodes__(G: nx.DiGraph, T: nx.DiGraph, nodes, visited, iterator):
    queue = []

    for node in nodes:
        for next_node in iterator(G, node):
            if next_node not in visited:
                T.add_edge(node, next_node)
                queue.append(next_node)
                visited.add(next_node)

    return queue

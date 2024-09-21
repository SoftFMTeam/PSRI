import networkx as nx

from ccft.algorithms.alg_funcs import __networkx_iterator_neighbors__, __networkx_iterator_succ__, \
    __networkx_iterator_pred__
from ccft.core.constant import ENode, EExpand


def networkx_subgraph(
        G: nx.DiGraph,
        init_nodes: list,
        node_types: list[ENode] = None,
        direction: EExpand = EExpand.Successor,
        max_depth=-1,
        node_type_lag: str = 'node_type',
):
    if node_types is None:
        node_types = [1, 2, 3]

    visited = set(init_nodes)
    queue = list(init_nodes)

    nodes = list(init_nodes)

    iterator = __networkx_iterator_neighbors__
    if direction == EExpand.Successor:
        iterator = __networkx_iterator_succ__
    elif direction == EExpand.Predecessor:
        iterator = __networkx_iterator_pred__

    def __node_filter__(u):
        if G.nodes[u][node_type_lag] in node_types:
            return True
        return False

    depth = 0
    if max_depth > 0:
        def __condition__():
            if queue and max_depth > depth:
                return True
            return False
    else:
        def __condition__():
            if queue:
                return True
            return False

    while __condition__():
        depth += 1
        t_queue = []
        for node in queue:
            neighbors = iterator(G, node)
            print(neighbors)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue

                visited.add(neighbor)

                if __node_filter__(neighbor):
                    t_queue.append(neighbor)
                    nodes.append(neighbor)
        queue = t_queue

    return G.subgraph(nodes)

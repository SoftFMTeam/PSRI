import networkx as nx


def networkx_all_paths(G: nx.DiGraph, start, end, max_len=-1):
    if max_len > 0:
        return nx.all_simple_paths(G, start, end, max_len)
    else:
        return nx.all_simple_paths(G, start, end)


def networkx_shortest_path(G: nx.DiGraph, start, end):
    return nx.shortest_path(G, start, end)

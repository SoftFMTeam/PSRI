import networkx as nx


def get_out_weights(graph: nx.DiGraph, node: str, weight_tag: str, w_successors_dict):
    """ Get the sum of the outgoing edge weights of the node """
    if node in w_successors_dict:
        return w_successors_dict[node]
    else:
        weight_total = 0.0
        for successor in graph.successors(node):
            weight_total += graph.get_edge_data(node, successor)[weight_tag]
        w_successors_dict[node] = weight_total

        return weight_total


def get_in_weights(graph: nx.DiGraph, node: str, weight_tag: str, w_predecessors_dict):
    """ Get the sum of the incoming edge weights of the node """
    if node in w_predecessors_dict:
        return w_predecessors_dict[node]
    else:
        weight_total = 0.0
        for predecessor in graph.predecessors(node):
            weight_total += graph.get_edge_data(predecessor, node)[weight_tag]
        w_predecessors_dict[node] = weight_total

        return weight_total


def cal_network_efficiency(G: nx.Graph):
    """ Efficiency of computational networks """
    totalW = 0.0
    for u, v, w in G.edges.data("weight", default=0):
        totalW += w

    N = G.number_of_nodes()
    return totalW / (N * (N-1))


def cal_network_complexity(G: nx.Graph):
    totalW = 0
    for n, w in G.nodes("weight", default=0):
        totalW += w

    N = G.number_of_nodes()
    return totalW / N

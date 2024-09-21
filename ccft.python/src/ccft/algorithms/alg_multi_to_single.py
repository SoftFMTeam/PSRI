import networkx as nx


def multi_to_single(
        G: nx.MultiDiGraph,
        weight_dict: dict,
        weight_lag: str,
        sum_flag: bool
):
    edges = []
    for source, target in G.edges():
        datas = G.get_edge_data(source, target)
        weight = 0.0
        relations = set()
        for data in datas.values():
            tag = data[weight_lag]
            if sum_flag or tag not in relations:
                relations.add(tag)
                weight += weight_dict[tag]

        edges.append((source, target, {'weight': round(weight, 3)}))

    graph = nx.DiGraph()
    graph.add_nodes_from(G.nodes(data=True))
    graph.add_edges_from(edges)
    return graph

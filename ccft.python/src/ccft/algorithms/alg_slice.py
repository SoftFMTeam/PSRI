import networkx as nx

from ccft.core.constant import ENode, ERelation, EExpand
from ccft.helper.network_index import NetworkxIndex


def networkx_edge_subgraph(
        G: nx.MultiDiGraph,
        relations: list[ERelation],
        relation_lag: str = 'r_key'
):
    if relations is None or len(relations) == 0:
        relations = [ERelation.Call, ERelation.Control, ERelation.Data]

    sub_edges = []
    for u, v, keys, attrs in G.edges(keys=True, data=True):
        if attrs[relation_lag] in relations:
            sub_edges.append((u, v, keys))

    # 边子图
    sub_edge_graph = G.edge_subgraph(sub_edges)

    return sub_edge_graph


def networkx_node_subgraph(
        G: nx.DiGraph,
        node_types: list[ENode],
        node_type_lag: str = 'node_type'
):
    # 提取所有符合要求的节点
    if node_types is None or len(node_types) == 0:
        node_types = [ENode.Method, ENode.Method, ENode.Local]

    sub_nodes = []
    for n, attrs in G.nodes(data=True):
        if attrs[node_type_lag] in node_types:
            sub_nodes.append(n)

    sub_node_graph = G.subgraph(sub_nodes)

    return sub_node_graph


def network_slice(
        G: nx.MultiDiGraph,
        graph_index: NetworkxIndex,
        start_nodes: list[int],
        node_types: list[ENode],
        edge_types: list[ERelation],
        direction: EExpand,
) -> nx.MultiDiGraph:
    sub_nodes = __gen_sub_nodes(G, graph_index, start_nodes, node_types, direction)
    sub_node_graph = G.subgraph(sub_nodes)

    sub_edges = __gen_sub_edges(graph_index, edge_types)
    sub_edge_graph = sub_node_graph.edge_subgraph(sub_edges)

    return sub_edge_graph


def __gen_sub_nodes(
        base_graph: nx.MultiDiGraph,
        graph_index: NetworkxIndex,
        start_nodes: list[int],
        node_types: list[ENode],
        direction: EExpand
):
    sub_nodes = []
    if not start_nodes:
        for node_type in node_types:
            sub_nodes.extend(graph_index.get_nodes(etp=node_type))
    else:
        appended_node_set: set[int] = set()
        handled_node_set: set[int] = set()
        queue = []

        queue.extend(start_nodes)

        while queue:
            front = queue.pop(0)

            if front in handled_node_set:
                continue

            handled_node_set.add(front)

            if not base_graph.has_node(front):
                continue

            data = base_graph.nodes[front]
            if not data['node_type'] in node_types:
                continue

            appended_node_set.add(front)

            if direction == EExpand.Predecessor or direction == EExpand.Dual:
                predecessors = base_graph.predecessors(front)
                for predecessor in predecessors:
                    if predecessor in handled_node_set:
                        continue
                    queue.append(predecessor)

            if direction == EExpand.Successor or direction == EExpand.Dual:
                successors = base_graph.successors(front)
                for successor in successors:
                    if successor in handled_node_set:
                        continue
                    queue.append(successor)

        sub_nodes = list(appended_node_set)
    return sub_nodes


def __gen_sub_edges(
        graph_index: NetworkxIndex,
        edge_types: list[ERelation]
):
    sub_edges = []
    for edge_type in edge_types:
        sub_edges.extend(graph_index.find_multi_edges(r_key=edge_type))

    return sub_edges

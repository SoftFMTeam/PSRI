import os

import networkx as nx
import pandas as pd

from ccft.core.constant import EnumNone, EEdgeWeight

node_keys_mapping = {
    'id': 'Id',
    'name': 'Name',
    'node_type': 'NodeType',
    'fullname': 'Fullname',
    'signature': 'Signature',
    'filename': 'Filename',
    'code': 'Code',
    'line_number': 'LineNumber',
    'line_number_end': 'LineNumberEnd',
    'column_number': 'ColumnNumber',
    'column_number_end': 'ColumnNumberEnd',
    'line_of_code': 'LineOfCode',
    'number_of_operators': 'NumberOfOperators',
    'set_of_operators': 'SetOfOperators',
    'number_of_operands': 'NumberOfOperands',
    'set_of_operands': 'SetOfOperands',
    'fan_in': 'FanIn',
    'fan_out': 'FanOut',
    'mc_cabe': 'McCabe',
    'acc_cyc': 'AccCyc',
    'con_cf': 'ConCf',
    'con_df': 'ConDf',
    'con_zf': 'ConZc',
    'con_rf': 'ConRf',
    'con_val': 'ConVal',
    'param': 'Parma',
    'param_in': 'ParmaIn',
    'param_out': 'ParmaOut',
    'ret_type': 'RetType',
}

edge_keys_mapping = {
    'source': 'Source',
    'target': 'Target',
    'line_number': 'LineNumber',
    'r_key': 'R_key',
    'r_label': 'R_label'
}


def network_save_graph_structure(
        graph: nx.DiGraph | nx.MultiDiGraph,
        data_dir: str,
        filename: str = None,
        save_nodes_edges: bool = True
):
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    if filename:
        nx.write_gexf(graph, f'{data_dir}\\{filename}.gexf')
        nx.write_graphml(graph, f'{data_dir}\\graph.graphml')
    else:
        nx.write_gexf(graph, f'{data_dir}\\graph.gexf')
        nx.write_graphml(graph, f'{data_dir}\\graph.graphml')

    if save_nodes_edges:
        network_save_nodes(graph, data_dir, filename)
        network_save_edges(graph, data_dir, filename)


def network_save_nodes(graph: nx.DiGraph | nx.MultiDiGraph, data_dir: str, filename: str = None):
    global node_keys_mapping

    node_datas = []
    for node, attrs in graph.nodes(data=True):
        attrs = {node_keys_mapping.get(key, key): value for key, value in attrs.items()}
        node_datas.append(attrs)

    node_df = pd.DataFrame(
        columns=['Id', 'Name', 'NodeType', 'Fullname', 'Signature', 'Filename', 'Code',
                 'LineNumber', 'LineNumberEnd', 'ColumnNumber', 'ColumnNumberEnd',
                 'LineOfCode',
                 'NumberOfOperators', 'SetOfOperators', 'NumberOfOperands', 'SetOfOperands',
                 'FanIn', 'FanOut', 'McCabe', 'AccCyc',
                 'ConCf', 'ConDf', 'ConZc', 'ConRf', 'ConVal',
                 'Parma', 'ParmaIn', 'ParmaOut', 'RetType'],
        data=node_datas,
    )
    if filename:
        node_df.to_csv(f'{data_dir}\\nodes_{filename}.csv')
    else:
        node_df.to_csv(f'{data_dir}\\nodes.csv')
    pass


def network_save_edges(graph: nx.DiGraph | nx.MultiDiGraph, data_dir: str, filename: str = None):
    global edge_keys_mapping

    edges_df = None
    if isinstance(graph, nx.MultiDiGraph):
        edge_datas = []
        for source, target, attrs in graph.edges(data=True):
            attrs = {edge_keys_mapping.get(key, key): value for key, value in attrs.items()}
            edge_datas.append(attrs)

        edges_df = pd.DataFrame(
            columns=['Source', 'Target', 'LineNumber', 'Relation', 'R_key', 'R_label'],
            data=edge_datas,
        )

    elif isinstance(graph, nx.DiGraph):
        edge_datas = []
        for source, target, attrs in graph.edges(data=True):
            attrs = {'Source': source, 'Target': target, 'Weight': attrs['weight']}
            edge_datas.append(attrs)

        edges_df = pd.DataFrame(
            columns=['Source', 'Target', 'Weight'],
            data=edge_datas,
        )
    if edges_df is not None:
        if filename:
            edges_df.to_csv(f'{data_dir}\\edges_{filename}.csv')
        else:
            edges_df.to_csv(f'{data_dir}\\edges.csv')
    pass


def network_multi_to_di(
        base_graph: nx.MultiDiGraph,
        edge_weights_tag: int = EnumNone) -> nx.DiGraph:
    graph = nx.DiGraph()

    if edge_weights_tag == EnumNone:
        for source, target, data in base_graph.edges(data=True):
            if not graph.has_edge(source, target):
                graph.add_edge(source, target, relation=data['r_key'])
            else:
                graph[source][target]['relation'] |= data['r_key']
    else:
        for source, target, data in base_graph.edges(data=True):
            if not graph.has_edge(source, target):
                graph.add_edge(source, target, relation=data['r_key'], weight=data['weight'])
            else:
                relation = graph[source][target]['relation']
                if edge_weights_tag == EEdgeWeight.Sum or (relation & data['r_key']) == 0:
                    graph[source][target]['weight'] += data['weight']

    return graph

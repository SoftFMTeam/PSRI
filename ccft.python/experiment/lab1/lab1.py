import os
import shutil

import networkx
import pandas
from loguru import logger
from scipy.stats import norm

from ccft.core.constant import ENode, ERelation
from ccft.service import service_save_graph
from ccft.util.utils import normalization, sorted_dict_values
from experiment.functions import func_load_graphs
from experiment.lab1.rank import my_rank, page_rank, element_rank

w_loc = 0.1
w_fan_in = 0.2
w_fan_out = 0.2
w_cc = 0.5


w_dict = {
    ERelation.Data: 0.3,
    ERelation.Control: 0.5,
    ERelation.Call: 0.2,
}


def main():
    lab_space = r'D:\Projects\CCFTools\demo\lab'
    for item in os.scandir(lab_space):
        if not item.is_dir():
            continue

        software_name = item.name
        lab_path = item.path

        logger.info(f'---------------- run {software_name} experiment 1 ----------------')

        neo4jcsv_path = os.path.join(lab_path, '.neo4jcsv')
        export_path = os.path.join(lab_path, '.lab1')

        GraphDict, NetworkIndex = func_load_graphs(
            neo4jcsv_path,
            lab_path,
            False
        )

        topic_graph = GraphDict['topic']

        comps, sum_comp, std_comps, degree_dict, in_degree_dict, out_degree_dict, edge_weights = (
            __gen_cal_graph__(topic_graph, export_path))

    pass


def __gen_cal_graph__(graph: networkx.MultiDiGraph, export_path: str):
    if os.path.isdir(export_path):
        shutil.rmtree(export_path)
    os.makedirs(export_path)

    node_comps = dict()
    total_comp = 0.0
    degree_dict = dict()
    in_degree_dict = dict()
    out_degree_dict = dict()
    for node_id, node_attrs in graph.nodes(data=True):
        _comp = __comp__(node_attrs)
        node_comps[node_id] = _comp
        total_comp += _comp
        degree_dict[node_id] = graph.degree(node_id)
        in_degree_dict[node_id] = graph.in_degree(node_id)
        out_degree_dict[node_id] = graph.out_degree(node_id)

    std_comp_dict = normalization(node_comps, False, True, True)

    edge_weights = dict()
    for source, target in graph.edges():
        weight = 0
        relations = set()
        for _, attrs in graph.get_edge_data(source, target).items():
            if attrs['r_key'] not in relations:
                weight += w_dict[attrs['r_key']]
                relations.add(attrs['r_key'])
        edge_weights[(source, target)] = weight

    return node_comps, total_comp, std_comp_dict, degree_dict, in_degree_dict, out_degree_dict, edge_weights


def fun(graph, node_comps, total_comp, std_comp_dict, degree_dict, in_degree_dict, out_degree_dict, edge_weights):
    nsr_dict, nid_dict = my_rank(graph, std_comp_dict, in_degree_dict, out_degree_dict)

    # page rank
    page_rank_dict = page_rank(graph)

    # element rank
    element_rank_dict = element_rank(graph, in_degree_dict, out_degree_dict)

    # Degree centrality
    dc = networkx.degree_centrality(graph)
    dc_dict = dict(zip(dc.keys(), dc.values()))
    logger.debug('Degree centrality calculations completed')

    # Betweenness Centrality
    bc = networkx.betweenness_centrality(graph, normalized=False, endpoints=True)
    std_bc_dict = dict(zip(bc.keys(), normalization(bc.values(), True, True, True)))
    logger.debug('Betweenness Centrality calculations completed')

    # Closeness Centrality
    cc = networkx.closeness_centrality(graph)
    cc_dict = dict(zip(cc.keys(), cc.values()))
    logger.debug('Closeness Centrality calculations completed')

    # k-core
    graph.remove_edges_from(networkx.selfloop_edges(graph))
    k_core_dict = networkx.algorithms.core_number(graph)
    logger.debug('k-core calculations completed')

    networkx.set_node_attributes(graph, degree_dict, '_degree')
    networkx.set_node_attributes(graph, in_degree_dict, '_in_degree')
    networkx.set_node_attributes(graph, out_degree_dict, '_out_degree')
    networkx.set_node_attributes(graph, std_comp_dict, '_comp')
    networkx.set_node_attributes(graph, dc_dict, '_dc')
    networkx.set_node_attributes(graph, cc_dict, '_cc')
    networkx.set_node_attributes(graph, std_bc_dict, '_bc')
    networkx.set_node_attributes(graph, nsr_dict, '_nsr')
    networkx.set_node_attributes(graph, nid_dict, '_nid')
    networkx.set_node_attributes(graph, page_rank_dict, '_page_rank')
    networkx.set_node_attributes(graph, element_rank_dict, '_element_rank')
    networkx.set_node_attributes(graph, k_core_dict, '_k_core')

    service_save_graph(export_path, 'lab1', graph, True)

    # log.print_debug('graph model', 'Export complete')
    # serialize_graph(graph, export_path, 'graph')
    # export_graph(graph, export_path, 'graph')
    # serialize_nodes(nodes, export_path)
    # serialize_edges(edges, export_path)
    # serialize(export_path, 'calc', graph)

    sorted_degrees = sorted_dict_values(degree_dict, True)
    sorted_in_degrees = sorted_dict_values(in_degree_dict, True)
    sorted_out_degrees = sorted_dict_values(out_degree_dict, True)
    sorted_comps = sorted_dict_values(node_comps, True)
    sorted_nid = sorted_dict_values(nid_dict, True)
    sorted_nsr = sorted_dict_values(nsr_dict, True)
    sorted_dc = sorted_dict_values(dc_dict, True)
    sorted_cc = sorted_dict_values(cc_dict, True)
    sorted_bc = sorted_dict_values(std_bc_dict, True)
    sorted_page_rank = sorted_dict_values(page_rank_dict, True)
    sorted_element_rank = sorted_dict_values(element_rank_dict, True)
    sorted_k_core_rank = sorted_dict_values(k_core_dict, True)

    measurements = pandas.DataFrame()
    measurements['degree'] = sorted_degrees[0]
    measurements['in_degree'] = sorted_in_degrees[0]
    measurements['out_degree'] = sorted_out_degrees[0]
    measurements['comp'] = sorted_comps[0]
    measurements['nid'] = sorted_nid[0]
    measurements['nsr'] = sorted_nsr[0]
    measurements['dc'] = sorted_dc[0]
    measurements['cc'] = sorted_cc[0]
    measurements['bc'] = sorted_bc[0]
    measurements['page_rank'] = sorted_page_rank[0]
    measurements['element_rank'] = sorted_element_rank[0]
    measurements['k_core_rank'] = sorted_k_core_rank[0]

    measurements.to_csv('%s\\measurements.csv' % export_path)
    logger.debug('Algorithmic ranking data export complete')

    # correlation analysis
    # tau, p_value = kendalltau(measurements['my_rank'], measurements['my_rank'])
    # print_debug('correlation analysis', 'my rank: tau %s, p value %s' % (tau, p_value))
    # tau, p_value = kendalltau(measurements['bc'], measurements['my_rank'])
    # print_debug('correlation analysis', 'bc: tau %s, p value %s' % (tau, p_value))
    # tau, p_value = kendalltau(measurements['dc'], measurements['my_rank'])
    # print_debug('correlation analysis', 'dc: tau %s, p value %s' % (tau, p_value))
    # tau, p_value = kendalltau(measurements['cc'], measurements['my_rank'])
    # print_debug('correlation analysis', 'cc: tau %s, p value %s' % (tau, p_value))
    # tau, p_value = kendalltau(measurements['page_rank'], measurements['my_rank'])
    # print_debug('correlation analysis', 'page_rank: tau %s, p value %s' % (tau, p_value))
    # tau, p_value = kendalltau(measurements['k_core_rank'], measurements['my_rank'])
    # print_debug('correlation analysis', 'k_core_rank: tau %s, p value %s' % (tau, p_value))
    # tau, p_value = kendalltau(measurements['element_rank'], measurements['my_rank'])
    # print_debug('correlation analysis', 'element_rank: tau %s, p value %s' % (tau, p_value))

    sir_df = pandas.DataFrame()
    initial_nodes = set()
    initial_nodes.update(tuple(sorted_nsr[0][:10]))
    initial_nodes.update(tuple(sorted_dc[0][:10]))
    initial_nodes.update(tuple(sorted_page_rank[0][:10]))
    initial_nodes.update(tuple(sorted_element_rank[0][:10]))

    # sir_values = sir(graph, initial_nodes)
    #
    # sir_df['my_rank'], sir_df['my_rank_val'] = f(graph, sorted_nsr[0][:10], sir_values)
    # sir_df['dc'], sir_df['dc_val'] = f(graph, sorted_dc[0][:10], sir_values)
    # sir_df['page_rank'], sir_df['page_rank_val'] = f(graph, sorted_page_rank[0][:10], sir_values)
    # sir_df['element_rank'], sir_df['element_rank_val'] = f(graph, sorted_element_rank[0][:10], sir_values)

    sir_df.to_csv('%s\\sir.csv' % export_path)
    logger.debug('Sir simulation data export completed')

    count_10 = int(0.1 * len(graph.nodes))
    my_rank_camp = 0.0
    for item in sorted_nsr[0][:count_10]:
        my_rank_camp += node_comps[item]
    dc_camp = 0.0
    for item in sorted_dc[0][:count_10]:
        dc_camp += node_comps[item]
    page_rank_camp = 0.0
    for item in sorted_page_rank[0][:count_10]:
        page_rank_camp += node_comps[item]
    element_rank_camp = 0.0
    for item in sorted_element_rank[0][:count_10]:
        element_rank_camp += node_comps[item]
    print('camps: my_rank %s, dc %s, page_rank %s, element_rank %s' % (
        my_rank_camp, dc_camp, page_rank_camp, element_rank_camp))
    print('rete : my_rank %s, dc %s, page_rank %s, element_rank %s' % (
        my_rank_camp / total_comp, dc_camp / total_comp, page_rank_camp / total_comp, element_rank_camp / total_comp))


def __comp__(attrs):
    """
    计算节点的复杂度

    :return: 节点复杂度
    """

    if attrs['node_type'] == ENode.Local or attrs['node_type'] == ENode.Member:
        return 0.0

    ex_loc = norm.cdf(attrs['line_of_code'], loc=100, scale=40)
    ex_fan_in = norm.cdf(attrs['fan_in'], loc=attrs['line_of_code'] * 0.5, scale=attrs['line_of_code'] * 0.1)
    ex_fan_out = norm.cdf(attrs['fan_out'], loc=attrs['line_of_code'] * 0.5, scale=attrs['line_of_code'] * 0.1)
    ex_cyclomatic_complexity = norm.cdf(attrs['acc_cyc'], loc=15, scale=4)

    comp = w_loc * ex_loc + w_fan_in * ex_fan_in + w_fan_out * ex_fan_out + w_cc * ex_cyclomatic_complexity

    return comp


def f(graph, nodes, sir_values):
    names = []
    values = []
    total = 0.0
    for node in nodes:
        names.append(graph.nodes[node]['name'])
        total += sir_values[node]
        values.append(sir_values[node])
    names.append('总计')
    values.append(total)

    return names, values


if __name__ == '__main__':
    main()

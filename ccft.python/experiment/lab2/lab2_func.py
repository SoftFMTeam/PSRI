import networkx
import numpy as np

from ccft.core.constant import ENode, ERelation

__all__ = [
    'lab2_calc_ncc',
    'lab2_calc_coupling_distance',
    'get_pdf'
]


def cal_nrc(
        graph,
        Eni,
        max_ncc,
):
    Nrc = dict.fromkeys(graph, 0.0)
    for node in graph.nodes():
        Nrc[node] = Eni[node] * graph.nodes[node]['weight'] / max_ncc

    return Nrc


def lab2_calc_ncc(graph: networkx.MultiDiGraph):
    nodes = list()
    labelDict = dict()
    typeDict = dict()

    for node, attrs in graph.nodes(data=True):
        H = 0
        V = 0

        n1 = 0
        n2 = 0
        N1 = 0
        N2 = 0

        if attrs['node_type'] == ENode.Method.value:
            ncc = attrs['fan_out'] + attrs['acc_cyc']
            N1 = attrs['number_of_operators']
            n1 = attrs['set_of_operators']
            N2 = attrs['number_of_operands']
            n2 = attrs['set_of_operands']
            N = N1 + N2
            n = n1 + n2
            log_n1 = np.log2(n1) if n1 > 0 else 0
            log_n2 = np.log2(n2) if n2 > 0 else 0
            log_n = np.log2(n) if n > 0 else 0
            H = n1 * log_n1 + n2 * log_n2
            V = N * log_n
        else:
            ncc = 1

        name = attrs['name']
        labelDict[node] = name
        nodeType = str(ENode(attrs['node_type']).name)
        typeDict[node] = nodeType

        nodes.append((node, {
            'id': node,
            'label': f'{name} ({node})',
            'node_type': nodeType,
            'weight': ncc,
            'fan_in': attrs['fan_in'],
            'fan_out': attrs['fan_out'],
            'sscc': attrs['acc_cyc'],
            'con_cf': attrs['con_cf'],
            'con_df': attrs['con_df'],
            'con_zc': attrs['con_zc'],
            'con_rf': attrs['con_rf'],
            'con_val': attrs['con_val'],
            'McCabe': attrs['mc_cabe'],
            'LOC': attrs['line_of_code'],
            'n1': n1,
            'n2': n2,
            'N1': N1,
            'N2': N2,
            'H': H,
            'V': V,
        }))

    return nodes, labelDict, typeDict


def lab2_calc_coupling_distance(graph: networkx.MultiDiGraph):
    maxWeight = -1
    edgeList = list()
    weightDict = dict()

    for source, target in graph.edges():
        edge_keys = graph[source][target]
        weight = 0
        for edge_key in edge_keys:
            succ_attrs = graph.get_edge_data(source, target, edge_key)
            if succ_attrs['r_key'] == ERelation.Control.value:
                weight += 4
            elif succ_attrs['r_key'] == ERelation.Value.value:
                weight += 3
            elif succ_attrs['r_key'] == ERelation.Data.value or succ_attrs['r_key'] == ERelation.Return.value:
                weight += 2.5
            elif succ_attrs['r_key'] == ERelation.Call.value:
                weight += 1
        if weight > maxWeight:
            maxWeight = weight
        weightDict[(source, target)] = weight
        edgeList.append((source, target, {
            'source': source,
            'target': target,
            'weight': weight,
            'label': weight,
        }))

    return edgeList, weightDict, maxWeight


def get_pdf(all_k):
    k = list(set(all_k))
    N = len(all_k)

    Pk = []
    for ki in sorted(k):
        c = 0
        for i in all_k:
            if i == ki:
                c += 1
        Pk.append(c / N)

    return sorted(k), Pk

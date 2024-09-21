import os
import shutil

import networkx as nx
import numpy as np
import pandas as pd
from loguru import logger
from networkx import DiGraph, MultiDiGraph
from scipy.optimize import curve_fit
from scipy.stats import kendalltau

from ccft.core.constant import ENode
from ccft.helper.network_index import NetworkxIndex
from ccft.service import service_load_graph, service_parse_cpg
from ccft.util.exceptions.error_code import ErrorCode
from ccft.util.exceptions.exception import CustomException
from ccft.util.utils import serialize_in_dir, deserialize, serialize
from experiment.algorithms.rank.anc_rank_ import alg_nac_rank0
from experiment.algorithms.rank.het_gm_rank import het_gm_rank
from experiment.algorithms.rank.page_rank_ import alg_page_rank
from experiment.lab2.lab2_func import lab2_calc_ncc, lab2_calc_coupling_distance

__all__ = [
    'func_load_graphs',
    'func_get_lab_graph',
    'func_std',
    'func_mul',
    'func_SortDictByValue',
    'func_KendallTauTest',
    'func_KendallTauTest_',
    'func_get_edge_influence',
    'save_graph'
]


def func_load_graphs(
        neo4jcsv_path: str,
        lab_path: str,
        reload=False
) -> tuple[dict[str, DiGraph | MultiDiGraph], NetworkxIndex]:
    if not os.path.isdir(neo4jcsv_path):
        raise CustomException(
            ErrorCode.Dir_NotFound,
            f'neo4jcsv code path \'{neo4jcsv_path}\' is not found',
            'lab2.export_graph')

    if not os.path.isdir(lab_path):
        os.mkdir(lab_path)

    basic_path = os.path.join(lab_path, 'basic')
    topic_path = os.path.join(lab_path, 'topic')

    if not reload and os.path.isdir(basic_path) and os.path.isdir(topic_path):
        logger.info("The graph data has been extracted and is currently loading...")
        graph_dict, network_index = service_load_graph(lab_path, dict())
        logger.info("Loading graph data completed")
    else:
        logger.info("Extracting graph data")
        graph_dict, network_index = service_parse_cpg(lab_path, neo4jcsv_path)
        logger.info("Image data extraction completed")

    return graph_dict, network_index


def func_get_lab_graph(modelDir, graphDir, softwareName, reload=False):
    neo4jcsv_path = os.path.join(modelDir, '.neo4jcsv')
    graphPath = os.path.join(graphDir, 'graph.bin')
    infoCsvPath = os.path.join(graphDir, 'info.csv')
    infoBinPath = os.path.join(graphDir, 'info.bin')
    labelBinPath = os.path.join(graphDir, 'labels.bin')
    typeBinPath = os.path.join(graphDir, 'types.bin')

    if reload or not os.path.isdir(graphDir):
        logger.info('Generate experimental image objects')

        if os.path.isdir(graphDir):
            shutil.rmtree(graphDir)
        os.mkdir(graphDir)

        GraphDict, NetworkIndex = func_load_graphs(
            neo4jcsv_path,
            modelDir,
            reload
        )
        topicGraph = GraphDict['topic']
        basicGraph = GraphDict['basic']
        nodeList, labelDict, typeDict = lab2_calc_ncc(topicGraph)
        edgeList, weightDict, maxWeight = lab2_calc_coupling_distance(topicGraph)
        labGraph = nx.DiGraph()
        labGraph.add_edges_from(edgeList)
        labGraph.add_nodes_from(nodeList)

        F = len(NetworkIndex.get_nodes(ENode.File))
        T = len(NetworkIndex.get_nodes(ENode.TypeDecl))
        M = len(NetworkIndex.get_nodes(ENode.Method))
        L = len(NetworkIndex.get_nodes(ENode.Local))
        P = len(NetworkIndex.get_nodes(ENode.Member))
        V = L + P
        BN = basicGraph.number_of_nodes()
        BE = basicGraph.number_of_edges()
        TN = topicGraph.number_of_nodes()
        TE = topicGraph.number_of_edges()
        LN = labGraph.number_of_nodes()
        LE = labGraph.number_of_edges()
        Loc = sum(data['LOC'] for n, data in labGraph.nodes(data=True))

        infoDict = {
            'Name': softwareName, 'File': F, 'LOC': Loc,
            'TypeDecl': T, 'Method': M, 'Local': L, 'Property': P, 'Variable': V,
            'Basic-Node': BN, 'Basic-Edge': BE, 'Topic-Node': TN,
            'Topic-Edge': TE, 'Lab-Node': LN, 'Lab-Edge': LE,
        }

        save_graph(graphDir, labGraph)
        infoDf = pd.DataFrame(data=infoDict, index=[0])
        infoDf.to_csv(infoCsvPath)
        serialize(labelBinPath, labelDict)
        serialize(typeBinPath, typeDict)
        serialize(infoBinPath, infoDict)
        logger.info(f'The experimental image object has been saved to the folder [{graphDir}]')

    else:
        logger.info('Loading experimental image objects')
        labGraph = deserialize(graphPath)
        labelDict = deserialize(labelBinPath)
        typeDict = deserialize(typeBinPath)
        infoDict = deserialize(infoBinPath)
        infoDf = pd.read_csv(infoCsvPath)

    return labGraph, labelDict, infoDict, typeDict


def func_get_histogram(data):
    min_val = min(data)
    max_val = max(data)
    counts, bins = np.histogram(data, bins=range(min_val, max_val + 1))
    return bins[:-1], counts


def func_curve_fit(func, x_data, y_data):
    p_opt, p_cov = curve_fit(func, x_data, y_data)

    y_pred = func(x_data, *p_opt)

    return p_opt, p_cov, y_pred


def func_std(vals: np.ndarray | list | dict):
    if isinstance(vals, np.ndarray):
        maxVal = np.max(vals)
        # minVal = np.min(vals)
        stdList = [val / maxVal for val in vals]
        return np.asarray(stdList)
    elif isinstance(vals, list):
        maxVal = np.max(vals)
        stdList = [val / maxVal for val in vals]
        return stdList
    elif isinstance(vals, dict):
        values = list(vals.values())
        maxVal = np.max(values)
        # minVal = np.min(values)
        stdDict = {k: v / maxVal for (k, v) in vals.items()}
        return dict(stdDict)


def func_mul(rank1, rank2):
    mulRank = dict()
    for node in rank1:
        mulRank[node] = rank1[node] * rank2[node]

    return mulRank


def save_graph(
        save_dir: str,
        graph: nx.DiGraph
):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    serialize_in_dir(save_dir, 'graph', graph)

    nx.write_gexf(graph, f'{save_dir}\\graph.gexf')
    nx.write_graphml(graph, f'{save_dir}\\graph.graphml')

    node_datas = []
    for node, attrs in graph.nodes(data=True):
        node_datas.append(attrs)

    node_df = pd.DataFrame(
        data=node_datas,
    )
    node_df.to_csv(f'{save_dir}\\nodes.csv')

    edge_datas = []
    for source, target, attrs in graph.edges(data=True):
        edge_datas.append(attrs)
    edges_df = pd.DataFrame(
        data=edge_datas,
    )
    edges_df.to_csv(f'{save_dir}\\edges.csv')
    pass


def func_SortDictByValue(adict):
    return dict(sorted(adict.items(), key=lambda item: item[1], reverse=True))


def func_KendallTauTest(_baseMethod_, _compares_, rate=None):
    SortedBaseSeq = func_SortDictByValue(_baseMethod_)
    baseIds = np.asarray(list(SortedBaseSeq.keys()))
    baseSeqs = np.asarray(list(SortedBaseSeq.values()))
    count = None
    if rate:
        if isinstance(rate, float) and 0 <= rate <= 1:
            count = int(len(_baseMethod_) * rate)
        elif isinstance(rate, int) and 0 < rate <= len(_baseMethod_):
            count = rate

        if count:
            baseIds = baseIds[:count]
            baseSeqs = baseSeqs[:count]

    _taus_ = dict()
    _pValues_ = dict()
    for methodName, compareMethod in _compares_:
        compareSeqs = np.asarray([compareMethod[n] for n in baseIds])

        tau, p_value = kendalltau(baseSeqs, compareSeqs)
        _taus_[methodName] = round(tau, 2)
        _pValues_[methodName] = round(p_value, 2)

    return _taus_, _pValues_


def func_KendallTauTest_(_compares_, rate=None):
    allTaus = dict()
    allPValues = dict()
    for methodName, compareMethod in _compares_:
        _baseMethod_ = compareMethod
        _taus_, _pValues_ = func_KendallTauTest(_baseMethod_, _compares_, rate)
        allTaus[methodName] = _taus_
        allPValues[methodName] = _pValues_

    return allTaus, allPValues


def func_get_edge_influence(G: nx.DiGraph, tag):
    influences = dict()
    if isinstance(tag, str):
        if tag == 'in-degree':
            for (u, v) in G.edges():
                influences[(u, v)] = 1.0 / G.in_degree(v)
        elif tag == 'out-degree':
            for (u, v) in G.edges():
                influences[(u, v)] = 1.0 / G.out_degree(u)
        elif tag == 'degree':
            for (u, v) in G.edges():
                influences[(u, v)] = 1.0 / G.degree(u)
        elif tag == 'w-in-degree':
            wInDict = dict()
            for (u, v) in G.edges():
                if v not in wInDict:
                    wInDict[v] = sum([G.get_edge_data(p, v)['weight'] for p in G.predecessors(v)])
                influences[(u, v)] = G.get_edge_data(u, v)['weight'] / wInDict[v]
        elif tag == 'w-out-degree':
            wOutDict = dict()
            for (u, v) in G.edges():
                if u not in wOutDict:
                    wOutDict[u] = sum([G.get_edge_data(u, s)['weight'] for s in G.successors(u)])
                influences[(u, v)] = G.get_edge_data(u, v)['weight'] / wOutDict[u]
        else:
            raise Exception('Influence setting error')
    elif isinstance(tag, float) and 0 <= tag <= 1:
        for (u, v) in G.edges():
            influences[(u, v)] = tag
    else:
        raise Exception('Influence setting error')

    return influences

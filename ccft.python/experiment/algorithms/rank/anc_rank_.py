import networkx as nx
import numpy as np


def alg_nac_rank0(G: nx.DiGraph, damping_factor=1):
    initVal, sumNcc, wInDict, wOutDict = __init_(G)
    rankVal = dict()
    accList = []

    def __cal_(u, dep):
        if u in rankVal:
            return rankVal[u]

        # 限制最大深度
        if dep > 10:
            return initVal[u]
        p = 0
        for s in G.successors(u):
            w = G.get_edge_data(u, s)['weight']
            p += w * __cal_(s, dep+1) / wOutDict[u]

        p *= damping_factor
        p += initVal[u]

        rankVal[u] = p
        accList.append(p)
        return p

    for node in G.nodes():
        __cal_(node, 0)

    return rankVal, np.asarray(accList)


def alg_nac_rank1(G: nx.DiGraph):
    initVal, sumNcc, wInDict, wOutDict = __init_(G)
    rankVal = dict()
    accList = []

    def __cal_(u, dep):
        if u in rankVal:
            return rankVal[u]

        if dep > 10:
            return initVal[u]

        p = initVal[u]
        for s in G.successors(u):
            w = G.get_edge_data(u, s)['weight']
            p += w * __cal_(s, dep+1) / wInDict[s]
        rankVal[u] = p
        accList.append(p)
        return p

    for node in G.nodes():
        __cal_(node, 0)

    return rankVal, np.asarray(accList)


def __init_(G):
    initVal = dict()
    sumNcc = 0.0
    wInDict = dict()
    wOutDict = dict()

    for node, node_data in G.nodes(data=True):
        ncc = node_data.get('weight', 1)
        initVal[node] = ncc
        sumNcc += ncc
        wInDict[node] = sum(G.get_edge_data(pred, node)['weight'] for pred in G.predecessors(node))
        wOutDict[node] = sum(G.get_edge_data(node, succ)['weight'] for succ in G.successors(node))

    return initVal, sumNcc, wInDict, wOutDict

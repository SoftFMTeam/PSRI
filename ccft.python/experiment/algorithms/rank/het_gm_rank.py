import networkx as nx

__all__ = [
    'het_gm_rank',
    'gc_rank',
    'ggc_rank',
    'gcd_rank',
    'ggcd_rank',
    'ksgc_rank'
]

import numpy as np


def het_gm_rank(
        G: nx.DiGraph,
        afos,
        afps,
        R=3,
        alpha=1,
        beta=1
):
    def _cal_gm(u, v, dis):
        r"""
            Calculate the gravitational force of node v on u
        """
        if u == v:
            return 0.0

        return afos[u] * afps[v] / (dis ** 2)

    def _dfs_pred_(srcNode, v, dis):
        r"""
            Depth-first traversal to compute gravitational values
        """
        if dis > R:
            return 0.0
        else:
            dfsGm = _cal_gm(v, srcNode, dis)
            for nextNode in G.predecessors(v):
                dfsGm += _dfs_pred_(srcNode, nextNode, dis + 1)
            return dfsGm

    def _dfs_succ_(srcNode, v, dis):
        if dis > R:
            return 0.0
        else:
            dfsGm = _cal_gm(srcNode, v, dis)
            for nextNode in G.successors(v):
                dfsGm += _dfs_succ_(srcNode, nextNode, dis + 1)
            return dfsGm

    gmRank = dict()

    for node, node_data in G.nodes(data=True):
        gm = 0.0
        if alpha:
            gm += _dfs_pred_(node, node, 0)
        if beta:
            gm += _dfs_succ_(node, node, 0)
        gmRank[node] = gm

    return gmRank


def gc_rank(
        G: nx.Graph,
        R=3,
):
    def _cal_gm(u, v, dis):
        if u == v:
            return 0.0

        return G.degree(u) * G.degree(v) / (dis ** 2)

    def _dfs_next_(srcNode, v, dis):
        if dis > R:
            return 0.0
        else:
            dfsGm = _cal_gm(srcNode, v, dis)
            for nextNode in G.neighbors(v):
                dfsGm += _dfs_next_(srcNode, nextNode, dis + 1)
            return dfsGm

    gmRank = dict()

    for node, node_data in G.nodes(data=True):
        gm = 0.0
        gm += _dfs_next_(node, node, 0)
        gmRank[node] = gm

    return gmRank


def gcd_rank(
        G: nx.DiGraph,
        R=3,
):
    def _cal_gm(u, v, dis):
        if u == v:
            return 0.0

        return G.degree(u) * G.degree(v) / (dis ** 2)

    def _dfs_next_(srcNode, v, dis):
        if dis > R:
            return 0.0
        else:
            dfsGm = _cal_gm(srcNode, v, dis)
            for nextNode in G.predecessors(v):
                dfsGm += _dfs_next_(srcNode, nextNode, dis + 1)
            return dfsGm

    gmRank = dict()

    for node, node_data in G.nodes(data=True):
        gm = 0.0
        gm += _dfs_next_(node, node, 0)
        gmRank[node] = gm

    return gmRank


def ggc_rank(
        G: nx.Graph,
        R=3,
        alpha=2
):
    def _sp_(u):
        k = G.degree(u)
        cv = clustering[u]
        sp = k * np.exp(-alpha * cv)
        return sp

    def _cal_gm(u, v, dis):
        if u == v:
            return 0.0

        return _sp_(u) * _sp_(v) / (dis ** 2)

    def _dfs_next_(srcNode, v, dis):
        if dis > R:
            return 0.0
        else:
            dfsGm = _cal_gm(srcNode, v, dis)
            for nextNode in G.neighbors(v):
                dfsGm += _dfs_next_(srcNode, nextNode, dis + 1)
            return dfsGm

    clustering = nx.clustering(G)
    gmRank = dict()

    for node, node_data in G.nodes(data=True):
        gm = 0.0
        gm += _dfs_next_(node, node, 0)
        gmRank[node] = gm

    return gmRank


def ggcd_rank(
        G: nx.DiGraph,
        R=3,
        alpha=2
):
    def _sp_(u):
        k = G.degree(u)
        cv = clustering[u]
        sp = k * np.exp(-alpha * cv)
        return sp

    def _cal_gm(u, v, dis):
        if u == v:
            return 0.0

        return _sp_(u) * _sp_(v) / (dis ** 2)

    def _dfs_next_(srcNode, v, dis):
        if dis > R:
            return 0.0
        else:
            dfsGm = _cal_gm(srcNode, v, dis)
            for nextNode in G.predecessors(v):
                dfsGm += _dfs_next_(srcNode, nextNode, dis + 1)
            return dfsGm

    clustering = nx.clustering(G)
    gmRank = dict()

    for node, node_data in G.nodes(data=True):
        gm = 0.0
        gm += _dfs_next_(node, node, 0)
        gmRank[node] = gm

    return gmRank


def iFit_rank(
        G: nx.DiGraph,
        prs,
        R=3,
):
    def _cal_gm(u, v, dis):
        if u == v:
            return 0.0

        return prs[u] * prs[v] / (dis ** 2)

    def _dfs_pred_(srcNode, v, dis):
        if dis > R:
            return 0.0
        else:
            dfsGm = _cal_gm(v, srcNode, dis)
            for nextNode in G.predecessors(v):
                dfsGm += _dfs_pred_(srcNode, nextNode, dis + 1)
            return dfsGm

    gmRank = dict()

    for node, node_data in G.nodes(data=True):
        gm = 0.0
        gm += _dfs_pred_(node, node, 0)
        gmRank[node] = gm

    return gmRank


def ksgc_rank(
        G: nx.DiGraph,
        R=3,
):
    def _cal_gm(u, v, dis):
        if u == v:
            return 0.0

        c = np.exp((ksDict[v] - ksDict[u]) / subKs)
        return c * degDict[u] * degDict[v] / (dis ** 2)

    def _dfs_pred_(srcNode, v, dis):
        if dis > R:
            return 0.0
        else:
            dfsGm = _cal_gm(v, srcNode, dis)
            for nextNode in G.predecessors(v):
                dfsGm += _dfs_pred_(srcNode, nextNode, dis + 1)
            return dfsGm

    gmRank = dict()

    ksMax = 0
    ksMin = 9999
    ksDict = dict()
    degDict = dict()
    for n in G.nodes:
        ks = nx.k_shell(G)
        ksDict[n] = ks
        ksMax = max(ksMax, ks)
        ksMin = min(ksMin, ks)
        degDict[n] = G.degree(n)
    subKs = ksMax - ksMin

    for node, node_data in G.nodes(data=True):
        gm = 0.0
        gm += _dfs_pred_(node, node, 0)
        gmRank[node] = gm

    return gmRank

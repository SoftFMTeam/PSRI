import os
import random
import sys

import networkx as nx
import pandas as pd
from loguru import logger
from matplotlib import pyplot as plt

from ccft.util.utils import sorted_dict_values


def main():
    _dir = os.path.dirname(sys.argv[0])
    s_index_path = os.path.join(_dir, 's-index.csv')
    r_index_path = os.path.join(_dir, 'r-index.csv')

    if os.path.exists(s_index_path) and os.path.exists(r_index_path):
        s_df = pd.read_csv(s_index_path)
        r_df = pd.read_csv(r_index_path)
        s_indexes = dict()
        r_indexes = dict()

        for idx in range(1, len(s_df.columns)):
            alg_name = s_df.columns[idx]
            s_indexes[alg_name] = list(s_df[alg_name])

        for idx in range(1, len(r_df.columns)):
            alg_name = r_df.columns[idx]
            r_indexes[alg_name] = list(r_df[alg_name])
    else:
        s_indexes, r_indexes = gen()

    rd_nodes = list(range(0, N))
    random.shuffle(rd_nodes)
    G_rd = get_graph()
    s_rd, r_rd = get_S_R_indexes(G_rd, rd_nodes)
    s_indexes['random'] = s_rd
    r_indexes['random'] = r_rd

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    logger.info('Draw an S-index chart')
    plot_indexes(ax1, s_indexes, 'Number of nodes deleted', 'S-index')
    logger.info('Draw an R-index chart')
    plot_indexes(ax2, r_indexes, 'Number of nodes deleted', 'R-index')
    fig.show()
    fig.savefig('plot.png')
    pass


def plot_indexes(subplot, indexes, x_label, y_label):
    x = range(0, N + 1)
    for alg_name, index in indexes.items():
        subplot.plot(x, index, label=alg_name)

    subplot.set_xlabel(x_label, fontdict={'fontsize': 20})
    subplot.set_ylabel(y_label, fontdict={'fontsize': 20})

    subplot.legend()
    pass


def gen():
    s_df = pd.DataFrame()
    s_indexes = dict()
    r_df = pd.DataFrame()
    r_indexes = dict()

    dc = nx.degree_centrality(G)
    sorted_dc, _ = sorted_dict_values(dc)
    G_dc = get_graph()
    s_dc, r_dc = get_S_R_indexes(G_dc, sorted_dc)
    s_indexes['DC'] = s_dc
    s_df['DC'] = s_dc
    r_indexes['DC'] = r_dc
    r_df['DC'] = r_dc
    logger.info('DC execution completed')

    pg = nx.pagerank(G)
    sorted_pg, _ = sorted_dict_values(pg)
    G_pg = get_graph()
    s_pg, r_pg = get_S_R_indexes(G_pg, sorted_pg)
    s_indexes['PageRank'] = s_pg
    s_df['PageRank'] = s_pg
    r_indexes['PageRank'] = r_pg
    r_df['PageRank'] = r_pg
    logger.info('PageRank execution completed')

    bc = nx.betweenness_centrality(G)
    sorted_bc, _ = sorted_dict_values(bc)
    G_bc = get_graph()
    s_bc, r_bc = get_S_R_indexes(G_bc, sorted_bc)
    s_indexes['BC'] = s_bc
    s_df['BC'] = s_bc
    r_indexes['BC'] = r_bc
    r_df['BC'] = r_bc
    logger.info('BC execution completed')

    s_df.to_csv('s-index.csv')
    r_df.to_csv('r-index.csv')

    return s_indexes, r_indexes


def get_graph():
    graph = nx.Graph()
    graph.add_nodes_from(G.nodes())
    graph.add_edges_from(G.edges())
    return graph


def get_S_R_index(graph):
    connected_components = nx.connected_components(graph)
    Nss = 0
    max_Ns = 0
    for connected_component in connected_components:
        Ns = len(connected_component)
        Nss += (Ns ** 2)
        if Ns > max_Ns:
            max_Ns = Ns
    S_index = (Nss - max_Ns ** 2) / N
    R_index = max_Ns / N
    return S_index, R_index


def get_S_R_indexes(graph, adict):
    s_index, r_index = get_S_R_index(graph)
    s_indexes = [s_index]
    r_indexes = [r_index]
    for idx in range(N):
        node = adict[idx]
        graph.remove_node(node)
        s_index, r_index = get_S_R_index(graph)
        s_indexes.append(s_index)
        r_indexes.append(r_index)
        pass

    return s_indexes, r_indexes


if __name__ == "__main__":
    N = 10000
    m = 4

    G = nx.barabasi_albert_graph(N, m)

    main()

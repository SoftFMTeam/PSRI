import networkx as nx
from matplotlib import pyplot as plt


def get_picture(G: nx.Graph, title='graph', label=None, edge_label=None, path=None):
    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, arrows=True)

    if label is not None:
        labels = dict()
        for node, data in G.nodes(data=True):
            labels[node] = data[label]
        nx.draw_networkx_labels(G, pos, labels=labels)

    if edge_label is not None:
        edge_labels = dict()
        for u, v, data in G.edges(data=True):
            edge_labels[u, v] = data[edge_label]
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(title)

    if path is None:
        plt.show()

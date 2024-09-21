import copy
from random import random

import networkx as nx

__all__ = ['sir_epidemic']


def sir_epidemic(
        G: nx.DiGraph,
        seeds: set | list,
        direction: str = 'back',
        beta=0.1,
        gamma=0.01,
        influence=None,
        step=100
):
    """
        Sir Simulation
        Parameters
        ----------
        G : networkx.DiGraph
            graphical object
        seeds: set|list
            initial set of nodes
        direction: str
            Node infection direction, for directed edge <u, v>, back: v infects u, front: u infects v, total: neighbor infects
        beta: float|dict
            Node infection rate, if float, infection rate is constant beta, if dict, infection rate is set to node attribute dict[node], default is 0.1
        gamma: float|dict
            Node recovery rate, if float, the recovery rate is a constant gamma, if dict, the recovery rate is set to the node attribute dict[node], default 0.01
        influence: dict
            Infectious capacity of the designated side
        step: int
            Number of iterations, default is 100
        Return
        ----------
        sirList : (s, i, r) list
            At the end of each iteration, the number of nodes in the s, i, and r states recorded
    """
    if isinstance(G, nx.MultiGraph):
        raise Exception("Polygonal map types are not supported")

    for s in seeds:
        if s not in G.nodes():
            raise Exception(f"The initial node [{s}] is not in the graph")

    if not G.is_directed():
        DG = G.to_directed()
    else:
        DG = copy.deepcopy(G)

    def _it_succ_(n):
        return G.successors(n)

    def _it_pred_(n):
        return G.predecessors(n)

    def _it_neigh_(n):
        return G.neighbors(n)

    if direction == 'back':
        _it_func_ = _it_succ_
    elif direction == 'front':
        _it_func_ = _it_pred_
    elif direction == 'total':
        _it_func_ = _it_neigh_
    else:
        raise Exception(f"Direction of infection incorrectly set")

    if isinstance(beta, float) and isinstance(gamma, float):
        return __sir_simulate_std__(
            graph=DG,
            seeds=seeds,
            beta=beta,
            gamma=gamma,
            steps=step,
            it_func=_it_func_
        )
    elif isinstance(beta, dict) and isinstance(gamma, dict):
        return __sir_simulate_dict__(
            graph=DG,
            seeds=seeds,
            betaDict=beta,
            gammaDict=gamma,
            steps=step,
            it_func=_it_func_
        )
    elif influence:
        return __sir_simulate_inf__(
            graph=DG,
            seeds=seeds,
            influence=influence,
            steps=step
        )
    else:
        raise Exception(f"Infection rate, recovery rate set abnormally")


def __sir_simulate_std__(graph, seeds, beta, gamma, steps, it_func):
    status = dict.fromkeys(graph.nodes(), 0)
    for node in seeds:
        status[node] = 1

    added_i_nodes_in_rounds = [[i for i in seeds]]
    count_i_in_rounds = [len(seeds)]
    i_nodes = list(seeds)

    for step in range(0, steps):
        newStatus = status.copy()
        i_nodes_in_this_round = []

        for node in graph.nodes():
            if status[node] == 0:
                for nextNode in it_func(node):
                    if status[nextNode] == 1:
                        rd = random()
                        if rd < beta:
                            newStatus[node] = 1
                            i_nodes_in_this_round.append(node)
                            i_nodes.append(node)
                            break
            elif gamma and status[node] == 1:
                rd = random()
                if rd < gamma:
                    status[node] = -1

        status = newStatus
        added_i_nodes_in_rounds.append(i_nodes_in_this_round)
        count_i_in_rounds.append(count_i(status))

    return i_nodes, count_i_in_rounds, added_i_nodes_in_rounds


def __sir_simulate_dict__(graph, seeds, betaDict, gammaDict, steps, it_func):
    status = dict.fromkeys(graph.nodes(), 0)
    for node in seeds:
        status[node] = 1

    added_i_nodes_in_rounds = [[i for i in seeds]]
    count_i_in_rounds = [len(seeds)]
    i_nodes = list(seeds)

    for step in range(steps):
        newStatus = status.copy()
        i_nodes_in_this_round = []

        for node in graph.nodes:
            if status[node] == 0:
                for nextNode in it_func(node):
                    if status[nextNode] == 1:
                        rd = random()
                        if rd < betaDict[node]:
                            newStatus[node] = 1
                            i_nodes_in_this_round.append(node)
                            i_nodes.append(node)
                            break
            elif status[node] == 1:
                rd = random()
                if rd < gammaDict[node]:
                    status[node] = -1

        status = newStatus
        added_i_nodes_in_rounds.append(i_nodes_in_this_round)
        count_i_in_rounds.append(count_i(status))

    return i_nodes, count_i_in_rounds, added_i_nodes_in_rounds


def __sir_simulate_inf__(graph, seeds, influence, steps):
    status = dict.fromkeys(graph.nodes(), 0)
    for node in seeds:
        status[node] = 1

    added_i_nodes_in_rounds = [[i for i in seeds]]
    count_i_in_rounds = [len(seeds)]
    i_nodes = list(seeds)

    for step in range(steps):
        newStatus = status.copy()
        i_nodes_in_this_round = []

        for node in graph.nodes:
            if status[node] == 0:
                for nextNode in graph.predecessors(node):
                    if status[nextNode] == 1:
                        rd = random()
                        if rd < influence[(nextNode, node)]:
                            newStatus[node] = 1
                            i_nodes_in_this_round.append(node)
                            i_nodes.append(node)
                            break
        status = newStatus
        added_i_nodes_in_rounds.append(i_nodes_in_this_round)
        count_i_in_rounds.append(count_i(status))

    return i_nodes, count_i_in_rounds, added_i_nodes_in_rounds


def count_i(Status):
    """ Calculation of the number of people in the three categories """
    i_count = 0
    for node, status in Status.items():
        if status == 1:
            i_count += 1

    return i_count

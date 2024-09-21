import copy

import networkx as nx

__all__ = ['linear_threshold']


def linear_threshold(
        G: nx.DiGraph,
        seeds: set | list,
        direction: str = 'back',
        thresholds: dict = None,
        influences: dict = None,
        steps=0
):
    """
    Parameters
    ----------
    G : networkx graph
        graphical object
    seeds: list of nodes
        initial set of nodes
    direction: str
        Node activation direction, for directed edges <u, v>, back: v activates u, front: u activates v
    steps: int
        Number of layers (depth) of activated nodes, when steps<=0, return all nodes that can be activated by the set of child nodes
    thresholds: dict
        Threshold for node activation
    influences: dict
        Influence of nodes
    Return
    ------
    layer_i_nodes : list of activated nodes
      layer_i_nodes[0]: the seeds
      layer_i_nodes[k]: the nodes activated at the kth diffusion step
    Notes
    -----
    1. Each node is supposed to have an attribute "threshold".  If not, the
       default value is given (0.5).
    2. Each edge is supposed to have an attribute "influence".  If not, the
       default value is given (1/in_degree)
    References
    ----------
    [1] GranovetterMark. Threshold models of collective behavior.
        The American journal of sociology, 1978.
    """

    if isinstance(G, nx.MultiGraph):
        raise Exception("Polygonal map types are not supported")

    for seed in seeds:
        if seed not in G.nodes():
            raise Exception(f"The initial node [{seed}] is not in the graph")

    if not G.is_directed():
        DG = G.to_directed()
    else:
        DG = copy.deepcopy(G)

    if thresholds is None:
        thresholds = dict()
        for node in DG.nodes():
            thresholds[node] = 0.5

    if direction == 'back':
        return _linear_threshold_back(DG, seeds, thresholds, influences, steps)
    elif direction == 'front':
        return _linear_threshold_front(DG, seeds, thresholds, influences, steps)
    else:
        raise Exception(f"Incorrect activation direction setting")


def _linear_threshold_front(G, seeds, thresholds, influences, steps):

    def _diffuse_all(_A_):
        _added_nodes_in_rounds_ = [[i for i in _A_]]
        _count_in_rounds_ = [len(_A_)]

        while True:
            len_old = len(_A_)
            _A_, activated_nodes_of_this_round = _diffuse_one_round(_A_)
            _added_nodes_in_rounds_.append(activated_nodes_of_this_round)
            _count_in_rounds_.append(len(_A_))
            if len(_A_) == len_old:
                break
        return _count_in_rounds_, _added_nodes_in_rounds_

    def _diffuse_k_rounds(_A_, _steps_):
        _added_nodes_in_rounds_ = [[i for i in _A_]]
        _count_in_rounds_ = [len(_A_)]
        while _steps_ > 0 and len(_A_) < len(G):
            len_old = len(_A_)
            _A_, activated_nodes_of_this_round = _diffuse_one_round(_A_)
            _added_nodes_in_rounds_.append(activated_nodes_of_this_round)
            _count_in_rounds_.append(len(_A_))
            if len(_A_) == len_old:
                break
            _steps_ -= 1
        return _count_in_rounds_, _added_nodes_in_rounds_

    def _diffuse_one_round(_activatedNodes_):
        def _influence_sum_(predNodes, to):
            influence_sum = 0.0
            for pred in predNodes:
                influence_sum += influences[(pred, to)]
            return influence_sum

        activated_nodes_of_this_round = set()
        for _acNode_ in _activatedNodes_:
            for succ in G.successors(_acNode_):
                if succ in _activatedNodes_:
                    continue
                pred_an = list(set(G.predecessors(succ)).intersection(set(_activatedNodes_)))
                if _influence_sum_(pred_an, succ) >= thresholds[succ]:
                    activated_nodes_of_this_round.add(succ)
        _activatedNodes_.extend(list(activated_nodes_of_this_round))
        return _activatedNodes_, list(activated_nodes_of_this_round)

    if influences is None:
        influences = dict()
        for (u, v) in G.edges():
            influences[(u, v)] = 1.0 / G.in_degree(v)

    A = copy.deepcopy(seeds)
    if steps <= 0:
        count_in_rounds, added_nodes_in_rounds = _diffuse_all(A)
    else:
        count_in_rounds, added_nodes_in_rounds = _diffuse_k_rounds(A, steps)

    return A, count_in_rounds, added_nodes_in_rounds


def _linear_threshold_back(G: nx.DiGraph, seeds, thresholds, influences, steps):

    def _diffuse_all(_A_):
        _added_nodes_in_rounds_ = [[i for i in _A_]]
        _count_in_rounds_ = [len(_A_)]

        while True:
            len_old = len(_A_)
            _A_, activated_nodes_of_this_round = _diffuse_one_round(_A_)
            _added_nodes_in_rounds_.append(activated_nodes_of_this_round)
            _count_in_rounds_.append(len(_A_))

            if len(_A_) == len_old:
                break

        return _count_in_rounds_, _added_nodes_in_rounds_

    def _diffuse_k_rounds(_A_, _steps_):
        _added_nodes_in_rounds_ = [[i for i in _A_]]
        _count_in_rounds_ = [len(_A_)]

        while _steps_ > 0 and len(_A_) < len(G):
            len_old = len(_A_)
            _A_, activated_nodes_of_this_round = _diffuse_one_round(_A_)
            _added_nodes_in_rounds_.append(activated_nodes_of_this_round)
            _count_in_rounds_.append(len(_A_))
            if len(_A_) == len_old:
                break
            _steps_ -= 1
        return _count_in_rounds_, _added_nodes_in_rounds_

    def _diffuse_one_round(_activatedNodes_):
        def _influence_sum_(succNodes, to):
            influence_sum = 0.0
            for succ in succNodes:
                influence_sum += influences[(to, succ)]
            return influence_sum

        activated_nodes_of_this_round = set()
        for _acNode_ in _activatedNodes_:
            for pred in G.predecessors(_acNode_):
                if pred in _activatedNodes_:
                    continue
                succ_an = list(set(G.successors(pred)).intersection(set(_activatedNodes_)))
                if _influence_sum_(succ_an, pred) >= thresholds[pred]:
                    activated_nodes_of_this_round.add(pred)
        _activatedNodes_.extend(list(activated_nodes_of_this_round))
        return _activatedNodes_, list(activated_nodes_of_this_round)

    if influences is None:
        influences = dict()
        for (u, v) in G.edges():
            influences[(u, v)] = 1.0 / G.out_degree(u)

    A = copy.deepcopy(seeds)
    if steps <= 0:
        count_in_rounds, added_nodes_in_rounds = _diffuse_all(A)
    else:
        count_in_rounds, added_nodes_in_rounds = _diffuse_k_rounds(A, steps)

    return A, count_in_rounds, added_nodes_in_rounds

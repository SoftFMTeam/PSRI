import networkx as nx
from loguru import logger


def alg_page_rank(
        G: nx.DiGraph,
        nodeTag: str = 'weight',
        edgeTag: str = 'weight',
        first_cal: str = 'count',
        direction: str = 'pre',
        damping_factor=0.85,
        max_iterations=100,
        tolerance=1e-7
) -> tuple[dict, dict, dict]:
    def _fir_ncc_():
        return G.nodes[node]['weight'] / sumNcc

    def _fir_count_():
        return 1 / G.number_of_nodes()

    def _fir_weight_in_():
        return wInDict[node] / sumWIn

    def _fir_weight_out_():
        return wOutDict[node] / sumWOut

    def _fir_weight_():
        return (wInDict[node] + wOutDict[node]) / sumW

    def _fir_degree_():
        return G.degree(node) / sumDeg

    def _fir_degree_out_():
        return G.out_degree(node) / sumOutDeg

    def _fir_degree_in_():
        return G.in_degree(node) / sumInDeg

    def _fir_zero_():
        return 0.0

    def _fir_weight_degree_():
        return ((wInDict[node] + wOutDict[node]) * G.degree(node)) / (sumW * sumDeg)

    def _sec_pred_(u):
        return preRankVal[u] * G.get_edge_data(u, node)[edgeTag] / wOutDict[u]

    def _sec_succ_(u):
        return preRankVal[u] * G.get_edge_data(node, u)[edgeTag] / wInDict[u]

    def _it_pred_(n):
        return G.predecessors(n)

    def _it_succ_(n):
        return G.successors(n)

    _func_fir_ = _fir_count_
    if first_cal == 'ncc':
        _func_fir_ = _fir_ncc_
    elif first_cal == 'zero':
        _func_fir_ = _fir_zero_
    elif first_cal == 'degree':
        _func_fir_ = _fir_degree_
    elif first_cal == 'degree-in':
        _func_fir_ = _fir_degree_in_
    elif first_cal == 'degree-out':
        _func_fir_ = _fir_degree_out_
    elif first_cal == 'weight':
        _func_fir_ = _fir_weight_
    elif first_cal == 'weight-in':
        _func_fir_ = _fir_weight_in_
    elif first_cal == 'weight-out':
        _func_fir_ = _fir_weight_out_
    elif first_cal == 'count':
        _func_fir_ = _fir_count_
    elif first_cal == 'weight_degree':
        _func_fir_ = _fir_weight_degree_

    _func_iterator_ = _it_pred_
    _func_sec_ = _sec_pred_
    if direction != 'pre':
        _func_iterator_ = _it_succ_
        _func_sec_ = _sec_succ_

    logger.debug('The node forward influence index begins to be calculated...')

    a = damping_factor
    b = 1 - damping_factor
    rankVal = dict()
    firDict = dict()
    secDict = dict()
    sumNcc = 0
    sumDeg = 0
    sumInDeg = 0
    sumOutDeg = 0
    sumW = 0.0
    sumWIn = 0.0
    sumWOut = 0.0
    wInDict = dict()
    wOutDict = dict()
    node_init_val = 1 / G.number_of_nodes()

    for node, node_data in G.nodes(data=True):
        rankVal[node] = node_init_val
        sumNcc += node_data[nodeTag]
        sumDeg += G.degree(node)
        sumInDeg += G.in_degree(node)
        sumOutDeg += G.out_degree(node)
        inW = sum(G.get_edge_data(pred, node)['weight'] for pred in G.predecessors(node))
        wInDict[node] = inW
        outW = sum(G.get_edge_data(node, succ)['weight'] for succ in G.successors(node))
        wOutDict[node] = outW
        sumWIn += inW
        sumWOut += outW
        sumW += (inW + outW)

    for it in range(max_iterations):
        preRankVal = rankVal.copy()
        sum_diff = 0

        for node, node_data in G.nodes(data=True):
            val = 0.0
            if b:
                firVal = _func_fir_()
                firDict[node] = firVal
                val += b * firVal
            if a:
                secVal = 0.0
                for nextNode in _func_iterator_(node):
                    tVal = _func_sec_(nextNode)
                    secVal += tVal
                secDict[node] = secVal
                val += a * secVal
            rankVal[node] = val
            sum_diff += abs(val - preRankVal[node])

        logger.debug('Number of iterations%s，inaccuracies%s' % (it, sum_diff))
        if sum_diff < tolerance:
            break

    logger.debug('Node Forward Influence Index Calculation Complete')

    return rankVal, firDict, secDict

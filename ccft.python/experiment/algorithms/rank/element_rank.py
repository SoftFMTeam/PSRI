import networkx as nx


__all__ = [
    'element_rank',
    'pr_rank'
]


def element_rank(
        G: nx.DiGraph,
        damping_factor=0.85,
        max_iterations=100,
        tolerance=1e-7
):
    prVals = dict()
    node_init_val = 1 / G.number_of_nodes()
    a = damping_factor
    b = 1 - damping_factor
    wOutDict = dict()
    wInDict = dict()
    sumWIn = 0.0

    for n, data in G.nodes(data=True):
        prVals[n] = node_init_val
        inW = sum(G.get_edge_data(pred, n)['weight'] for pred in G.predecessors(n))
        outW = sum(G.get_edge_data(n, succ)['weight'] for succ in G.successors(n))
        wOutDict[n] = outW
        wInDict[n] = inW
        sumWIn += inW

    it = 0
    while True:
        preRankVal = prVals.copy()
        sum_diff = 0

        for n, data in G.nodes(data=True):
            val = 0.0
            if b:
                firVal = wInDict[n] / sumWIn
                val += b * firVal
            if a:
                secVal = 0.0
                for p in G.predecessors(n):
                    tVal = preRankVal[p] * G.get_edge_data(p, n)['weight'] / wOutDict[p]
                    secVal += tVal
                val += a * secVal

            prVals[n] = val
            sum_diff += abs(val - preRankVal[n])

        if sum_diff < tolerance or it > max_iterations:
            break

    return prVals


def pr_rank(
        G: nx.DiGraph,
        damping_factor=0.85,
        max_iterations=100,
        tolerance=1e-7
):
    prVals = dict()
    node_init_val = 1 / G.number_of_nodes()
    a = damping_factor
    b = 1 - damping_factor

    wOutDict = dict()
    wDegDict = dict()
    degDict = dict()

    sumDeg = 0
    sumWDeg = 0.0

    for n, data in G.nodes(data=True):
        prVals[n] = node_init_val
        inW = sum(G.get_edge_data(pred, n)['weight'] for pred in G.predecessors(n))
        outW = sum(G.get_edge_data(n, succ)['weight'] for succ in G.successors(n))
        wOutDict[n] = outW
        wDeg = inW + outW
        wDegDict[n] = wDeg
        sumWDeg += wDeg
        deg = G.degree(n)
        degDict[n] = deg
        sumDeg += deg

    it = 0
    while True:
        preRankVal = prVals.copy()
        sum_diff = 0

        for n, data in G.nodes(data=True):
            val = 0.0
            if b:
                firVal = (wDegDict[n] * degDict[n]) / (sumWDeg * sumDeg)
                val += b * firVal
            if a:
                secVal = 0.0
                for p in G.predecessors(n):
                    tVal = preRankVal[p] * G.get_edge_data(p, n)['weight'] / wOutDict[p]
                    secVal += tVal
                val += a * secVal

            prVals[n] = val
            sum_diff += abs(val - preRankVal[n])

        if sum_diff < tolerance or it > max_iterations:
            break

    return prVals

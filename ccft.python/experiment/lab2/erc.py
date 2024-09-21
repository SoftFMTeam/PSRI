from heapq import heappush, heappop
from itertools import count


def cal_nrc(
        graph,
        Eni,
        max_ncc,
        total_ncc
):
    Nrc = dict.fromkeys(graph, 0.0)
    for node in graph.nodes():
        Nrc[node] = Eni[node] * graph.nodes[node]['weight'] / max_ncc

    return Nrc


def cal_eni(
        graph,
        weight: str = 'weight',
        distance: str = 'distance',
        normalized: bool = True,
        endpoints: bool = True,
):
    Eni = dict.fromkeys(graph, 0.0)
    nodes = graph

    for s in nodes:
        # single source shortest paths
        S, Pre, Sigma, Dist, WSigma, WPath = _single_source_dijkstra_path_basic(graph, s, weight, distance)
        # accumulation
        if endpoints:
            Eni, _1 = _accumulate_endpoints_w(Eni, S, WSigma, WPath, s)
        else:
            Eni, _0 = _accumulate_basic_w(Eni, S, WSigma, WPath, s)

    # rescaling
    Eni = _rescale(
        Eni,
        len(graph),
        normalized=normalized,
        directed=graph.is_directed(),
        endpoints=True,
    )
    return Eni


def _single_source_dijkstra_path_basic(graph, s, weight, distance):
    c = count()
    Heap = []
    S = []
    Pre = dict()
    '''{ node : [pre node of node]} | node in S'''
    WPath = dict()
    '''{ node : { t : [(sp-s..->node, wpath(sp-s..->node))] }} '''
    WSigma = dict.fromkeys(graph, 0.0)
    '''{ node : wpath(sp-s..->v) }'''
    Dist = {}
    '''{ node : dist(sp-s..->node) } | node in S'''
    seen = {s: 0}

    for node in graph.nodes():
        Pre[node] = []
        WPath[node] = []

    WPath[s].append(([], 0))

    heappush(Heap, (0, 0, 0, next(c), s, s))
    while Heap:
        (dist, wpath, wedge, it, pre, cur) = heappop(Heap)
        if cur in Dist:
            continue

        S.append(cur)
        Dist[cur] = dist

        if cur != s:
            for it_path, it_wpath in WPath[pre]:
                cur_path = [pre]
                cur_path.extend(it_path)
                cur_wpath = it_wpath + wedge
                WPath[cur].append((cur_path, cur_wpath))
                WSigma[cur] += cur_wpath

        for succ, edge_attr in graph[cur].items():
            vw_dist = dist + edge_attr[distance]
            w_edge = edge_attr[weight]
            vw_wpath = wpath + w_edge

            if succ not in Dist and (succ not in seen or vw_dist < seen[succ]):
                seen[succ] = vw_dist
                heappush(Heap, (vw_dist, vw_wpath, w_edge, next(c), cur, succ))
                Pre[succ] = [cur]
            elif vw_dist == seen[succ]:
                Pre[succ].append(cur)

                for it_path, it_wpath in WPath[cur]:
                    succ_path = [cur]
                    succ_path.extend(it_path)
                    succ_wpath = it_wpath + w_edge
                    WPath[succ].append((succ_path, succ_wpath))
                    WSigma[succ] += succ_wpath

    return S, Pre, WSigma, Dist, WSigma, WPath


def _accumulate_endpoints_w(betweenness, S, WSigma, WPath, s):
    betweenness[s] += len(S) - 1
    delta = dict.fromkeys(S, 0)
    while S:
        t = S.pop()
        if t != s:
            coeff = 1 / WSigma[t]
            for path, wp in WPath[t]:
                for pre in path:
                    delta[pre] += wp * coeff
            betweenness[t] += delta[t] + 1
    return betweenness, delta


def _accumulate_basic_w(betweenness, S, WSigma, WPath, s):
    delta = dict.fromkeys(S, 0)
    while S:
        t = S.pop()
        for path, wp in WPath[t]:
            for pre in path:
                delta[pre] += wp / WSigma[t]
        if t != s:
            betweenness[t] += delta[t]
    return betweenness, delta


def _rescale(betweenness, n, normalized, directed=False, k=None, endpoints=False):
    if normalized:
        if endpoints:
            if n < 2:
                scale = None  # no normalization
            else:
                # Scale factor should include endpoint nodes
                scale = 1 / (n * (n - 1))
        elif n <= 2:
            scale = None  # no normalization b=0 for all nodes
        else:
            scale = 1 / ((n - 1) * (n - 2))
    else:  # rescale by 2 for undirected graphs
        if not directed:
            scale = 0.5
        else:
            scale = None
    if scale is not None:
        if k is not None:
            scale = scale * n / k
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness

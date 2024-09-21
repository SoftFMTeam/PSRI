import networkx
from loguru import logger

from experiment.algorithms.utils import get_in_weights, get_out_weights


def my_rank(
        graph: networkx.DiGraph,
        comp_dict: dict,
        edge_weights: dict,
        w_predecessors_dict=None,
        w_successors_dict=None,
        damping_factor=0.85,
        max_iterations=50,
        tolerance=1e-6
) -> tuple[dict, dict]:
    logger.debug('my_rank starts iterating...')

    a = damping_factor
    b = 1 - damping_factor
    number_of_nodes = graph.number_of_nodes()
    node_init_val = 1 / number_of_nodes

    nid = dict()
    nsr = dict()

    sum_comp = 0

    if w_predecessors_dict is None:
        w_predecessors_dict = dict()
    if w_successors_dict is None:
        w_successors_dict = dict()

    for node in graph.nodes:
        nsr[node] = node_init_val
        get_in_weights(graph, node, w_predecessors_dict, 'weight')
        get_out_weights(graph, node, w_successors_dict, 'weight')
        sum_comp += comp_dict[node]

    for iteration in range(max_iterations):
        prev_my_rank_values = nsr.copy()
        sum_diff = 0

        for node in graph.nodes:
            h_in = 0
            for predecessor in graph.predecessors(node):
                weight = graph.get_edge_data(predecessor, node)['weight']
                h_in += prev_my_rank_values[predecessor] * weight / w_successors_dict[predecessor]

            h_cmp = comp_dict[node] / sum_comp
            # for successor_id in graph.successors(node):
            #     weight = graph.get_edge_data(node, successor_id)['weight']
            #     h_cmp += prev_my_rank_values[successor_id] * weight
            # if w_successors_dict[node]:
            #     h_cmp = h_cmp / w_successors_dict[node]

            h = (a * h_in + b * h_cmp)
            # h = (a * h_in + b * h_cmp)

            nid[node] = h_in
            nsr[node] = h

            sum_diff += abs(h - prev_my_rank_values[node])

        logger.debug('my_rank iterations%s，inaccuracies%s' % (iteration, sum_diff))
        if sum_diff < tolerance:
            break

    logger.debug('my_rank calculation is complete')
    return nsr, nid


def page_rank(graph: networkx.DiGraph, damping_factor=0.85, max_iterations=100, tolerance=1e-6):
    logger.debug('pagerank started iterating...')

    a = damping_factor
    b = 1 - damping_factor
    number_of_nodes = graph.number_of_nodes()
    node_init_val = 1 / number_of_nodes
    pagerank_values = {node: node_init_val for node in graph}

    for iteration in range(max_iterations):
        prev_pagerank_values = pagerank_values.copy()
        sum_diff = 0

        for node in graph.nodes:
            pagerank_values[node] = b / number_of_nodes
            for incoming_node in graph.predecessors(node):
                pagerank_values[node] += a * prev_pagerank_values[incoming_node] / graph.out_degree(incoming_node)

            sum_diff += abs(pagerank_values[node] - prev_pagerank_values[node])

        logger.debug('pagerank iterations%s，inaccuracies%s' % (iteration, sum_diff))
        if sum_diff < tolerance:
            break
    logger.debug('pagerank calculation is complete')
    return pagerank_values


def element_rank(graph: networkx.DiGraph, w_predecessors_dict=None, w_successors_dict=None, damping_factor=0.85,
                 max_iterations=100, tolerance=1e-6):
    logger.debug('element_rank started iterating...')

    a = damping_factor
    b = 1 - damping_factor
    number_of_nodes = graph.number_of_nodes()
    node_init_val = 1 / number_of_nodes

    element_rank_values = dict()

    if w_predecessors_dict is None:
        w_predecessors_dict = dict()
    if w_successors_dict is None:
        w_successors_dict = dict()
    sum_w_predecessors = 0

    for node in graph.nodes:
        element_rank_values[node] = node_init_val
        sum_w_predecessors += get_in_weights(graph, node, w_predecessors_dict, 'weight')
        get_out_weights(graph, node, w_successors_dict, 'weight')

    for iteration in range(max_iterations):
        prev_element_rank_values = element_rank_values.copy()
        sum_diff = 0

        for node in graph.nodes:
            element_rank_values[node] = b * w_predecessors_dict[node] / sum_w_predecessors
            for predecessor in graph.predecessors(node):
                weight = graph.get_edge_data(predecessor, node)['weight']
                element_rank_values[node] += a * prev_element_rank_values[predecessor] * weight / w_successors_dict[
                    predecessor]

            sum_diff += abs(element_rank_values[node] - prev_element_rank_values[node])

        logger.debug('element_rank iterations%s，inaccuracies%s' % (iteration, sum_diff))
        if sum_diff < tolerance:
            break
    logger.debug('element_rank calculation is complete')
    return element_rank_values

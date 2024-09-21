import random

import networkx


def sir(graph: networkx.DiGraph, initial_nodes: set, beta=0.1, gamma=0.01, days=50) -> dict[str, int]:
    sir_count = dict()
    for node in initial_nodes:
        sir_count[node] = sir_simulate(graph, node, beta, gamma, days)
    return sir_count


def sir_simulate(graph: networkx.DiGraph, initial_node: str, beta=0.1, gamma=0.01, days=50):
    """
    Sir simulation
    :param graph:
    :param initial_node: initial infected node
    :param beta: infection rate
    :param gamma: recovery rate
    :param days: simulation days
    :return:
    """
    days = 50  # Setting the number of days for simulation
    beta = 0.1

    for node in graph.nodes():
        graph.nodes[node]['status'] = 'S'
    graph.nodes[initial_node]['status'] = 'I'

    sir_list = []
    for _ in range(0, days):
        for node in graph.nodes:
            rd = random.random()
            if graph.nodes[node]['status'] != 'I':
                p_suc = 0.0
                for successor in graph.successors(node):
                    if graph.nodes[successor]['status'] == 'I':
                        p_suc += (graph.get_edge_data(node, successor)['weight'])
                if p_suc:
                    p_suc /= graph.out_degree(node)
                p_pre = 0.0
                for predecessors in graph.predecessors(node):
                    if graph.nodes[predecessors]['status'] == 'I':
                        p_pre += graph.get_edge_data(predecessors, node)['weight']
                if p_pre:
                    p_pre /= graph.in_degree(node)
                p = beta * (0.15 * p_pre + 0.85 * p_suc)

                if rd < p:
                    graph.nodes[node]['status'] = 'I'
            else:
                if rd < gamma:
                    graph.nodes[node]['status'] = 'R'

        sir_list.append(countSIR(graph))
    return countSIR(graph)


def simulate_spread(graph, beta):
    for node in graph.nodes:
        if graph.nodes[node]['status'] != 'I':
            out_degree = graph.out_degree(node)
            in_degree = graph.in_degree(node)
            p_suc = 0
            p_pre = 0

            if out_degree:
                i_successors = [n for n in graph.successors(node) if graph.nodes[n]['status'] == 'I']
                p_suc = len(i_successors) / out_degree
            if in_degree:
                i_predecessors = [n for n in graph.predecessors(node) if graph.nodes[n]['status'] == 'I']
                p_pre = len(i_predecessors) / in_degree

            p = 0.1 * graph.nodes[node]['_comp'] * (0.15 * p_pre + 0.85 * p_suc)

            if random.random() < p:
                graph.nodes[node]['status'] = 'I'


def countSIR(graph):
    i = 0
    for node in graph:
        if graph.nodes[node]["status"] == "I":
            i = i + 1
    return i


def sir_simulation_on_network(graph, infected_nodes, beta=0.1, gamma=0.01, days=50):
    """
    SIR model Complex network implementation
    :param graph: graph
    :param beta: infection rate
    :param gamma: recovery rate
    :param infected_nodes: initial infected node
    :param days: simulation days
    :return:
    """
    population = graph.number_of_nodes()
    susceptible_nodes = set(graph.nodes()) - set(infected_nodes)
    susceptible = len(susceptible_nodes)
    infected = len(infected_nodes)
    susceptible_list = [susceptible]
    infected_list = [infected]
    removed_list = [0]

    for day in range(days):
        new_infected = 0
        new_removed = 0

        for node in infected_nodes:
            neighbors = list(graph.neighbors(node))
            new_infected += beta * len(set(neighbors) & susceptible_nodes)
            new_removed += gamma

        susceptible -= new_infected
        infected += new_infected - new_removed

        susceptible_list.append(susceptible)
        infected_list.append(infected)
        removed_list.append(removed_list[-1] + new_removed)

    return susceptible_list, infected_list, removed_list

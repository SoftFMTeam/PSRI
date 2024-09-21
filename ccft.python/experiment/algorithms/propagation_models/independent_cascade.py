import copy
import random

import networkx as nx

__all__ = ['independent_cascade']


def independent_cascade(
        G: nx.DiGraph,
        seeds: set | list,
        direction: str = 'back',
        influences: dict = None,
        steps=0
):
    if isinstance(G, nx.MultiGraph):
        raise Exception("Polygonal map types are not supported")

    for seed in seeds:
        if seed not in G.nodes():
            raise Exception(f"The initial node [{seed}] is not in the graph")

    if not G.is_directed():
        DG = G.to_directed()
    else:
        DG = copy.deepcopy(G)

    # Specify the direction of propagation, for directed edges <u, v>, back: v activates u, front: u activates v
    if direction == 'back':
        return _independent_cascade_back(DG, seeds, influences, steps)
    elif direction == 'front':
        return _independent_cascade_front(DG, seeds, influences, steps)
    else:
        raise Exception(f"Incorrect activation direction setting")


def _independent_cascade_front(G, seeds, influences, steps):
    if influences is None:
        influences = dict()
        for (u, v) in G.edges():
            influences[(u, v)] = 1.0 / G.in_degree(v)
    else:
        if isinstance(influences, float) and 0 < influences <= 1:
            k = influences
            influences = {edge: k for edge in G.edges}

    active = set(seeds)
    newly_active = set(seeds)

    active_each_rounds = [list(newly_active)]
    count_in_rounds = [len(newly_active)]

    while newly_active and (steps == 0 or len(active_each_rounds) <= steps):
        current_step_active = set()
        for node in newly_active:
            for succ in G.successors(node):
                if succ not in active:
                    rand = random.random()
                    influence = influences[(node, succ)]
                    if rand < influence:
                        current_step_active.add(succ)
                        active.add(succ)
        newly_active = current_step_active
        active_each_rounds.append(list(newly_active))
        count_in_rounds.append(len(active))

    return active, count_in_rounds, active_each_rounds


def _independent_cascade_back(G, seeds, influences, steps):
    if influences is None:
        influences = dict()
        for (u, v) in G.edges():
            influences[(u, v)] = 1.0 / G.out_degree(u)
    else:
        if isinstance(influences, float) and 0 < influences <= 1:
            k = influences
            influences = {edge: k for edge in G.edges}

    active = set(seeds)
    newly_active = set(seeds)

    active_each_step = [list(newly_active)]
    count_in_rounds = [len(newly_active)]

    while newly_active and (steps == 0 or len(active_each_step) <= steps):
        current_step_active = set()
        for node in newly_active:
            for pred in G.predecessors(node):
                if pred not in active:
                    rand = random.random()
                    influence = influences[(pred, node)]
                    if rand < influence:
                        current_step_active.add(pred)
                        active.add(pred)
        newly_active = current_step_active
        active_each_step.append(list(newly_active))
        count_in_rounds.append(len(active))

    return active, count_in_rounds, active_each_step

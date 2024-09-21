import os
import pickle
import random
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool
from scipy.stats import kendalltau

from experiment.lab2._0_config_ import LabSpace
from experiment.functions import func_get_lab_graph
from experiment.algorithms.propagation_models.sir_epidemic import sir_epidemic


epoch = 1000
step = 100
beta = 0.10


def sim_simulation(parameter):
    graph, node = parameter
    infected_nodes_list = list()
    for _ in range(epoch):
        sim_nodes, sim_round_counts, sim_round_nodes = sir_epidemic(
            G=graph,
            seeds=[node],
            beta=beta,
            gamma=0.0,
            step=step
        )
        infected_nodes_list.append(len(sim_nodes))

    return [node, sum(infected_nodes_list) / len(infected_nodes_list)]


def build_dri_si_result(si_pkl_path: str, graph):
    nodes = list(graph.nodes())
    params = [(graph, node) for node in nodes]

    node_influence_list = list()
    with Pool(processes=8) as p:
        map_func = getattr(p, "imap_unordered")
        for ret in tqdm(map_func(sim_simulation, params, 10), total=len(nodes), desc="(8 Worker) sim_simulation"):
            node_influence_list.append(ret)

    node_influence_dict = dict()
    for node_influence in node_influence_list:
        node_influence_dict[node_influence[0]] = node_influence[1]

    node_influence = dict(sorted(node_influence_dict.items(), key=lambda item: item[1], reverse=True))
    with open(si_pkl_path, 'wb') as f:
        pickle.dump(node_influence, f)


def build_vri_si_result(si_pkl_path: str, graph):
    nodes = list(graph.nodes())
    node_infect_dict = {node: 0 for node in nodes}
    seed_number = int(len(nodes) * 0.05)

    for _ in tqdm(range(epoch), desc='Build VRI SI Result'):
        seeds = random.sample(nodes, seed_number)
        sim_nodes, sim_round_counts, sim_round_nodes = sir_epidemic(
            G=graph,
            seeds=seeds,
            beta=beta,
            gamma=0.0,
            step=step
        )
        for node in sim_nodes:
            node_infect_dict[node] = node_infect_dict[node] + 1

    node_infect = dict(sorted(node_infect_dict.items(), key=lambda item: item[1], reverse=True))
    with open(si_pkl_path, 'wb') as f:
        pickle.dump(node_infect, f)

def dri_kendall_correlation_coefficient(result_dir: str, software_graph):
    dri_method_dict = {
        'DC': 'dc',
        'Page Rank': 'pg',
        'BC': 'bc',
        'GC_d': 'gcd',
        'GGC_d': 'ggcd',
        'Element Rank': 'er',
        'Class Rank': 'cr',
        'iFit': 'iFit',
        'DRI': 'DRI',
    }
    baseline_methods = list(dri_method_dict.keys())

    for software, graph in software_graph.items():
        node_ids = list(graph.nodes())
        node_ids.sort()

        si_pkl_path = os.path.join(result_dir, 'si', f'{software}.pkl')
        if not os.path.exists(si_pkl_path):
            os.makedirs(si_pkl_path)
        with open(si_pkl_path, 'rb') as f:
            si_data = pickle.load(f)

        rank_result = dict()
        rank_result['SI'] = [si_data[node_id] for node_id in node_ids]

        for method in baseline_methods:
            node_data = dict(graph.nodes.data(dri_method_dict[method]))
            rank_result[method] = [node_data[node_id] for node_id in node_ids]

        software_df = pd.DataFrame(columns=['node_ratio'] + baseline_methods)
        for node_ratio in [0.125]:
            result_dict = dict()
            result_dict['node_ratio'] = node_ratio

            for method in baseline_methods:
                x = rank_result["SI"]
                x = x[: int(len(x) * node_ratio)]
                y = rank_result[method]
                y = y[: int(len(y) * node_ratio)]
                tau, p_value = kendalltau(x, y)
                result_dict[method] = round(tau, 3)
            software_df.loc[len(software_df)] = result_dict

        software_df.to_csv(os.path.join(result_dir, f'{software}.csv'), index=False)


def main():
    # software_names = ['LevelDB', 'Log4cxx', 'Memcached', 'Nginx', 'Node.js', 'Redis', 'Terminal', 'VLC']
    software_names = ['Node.js']
    software_graph = dict()

    for software in software_names:
        modelDir = os.path.join(LabSpace, software)
        labDir = os.path.join(modelDir, '.lab2')

        graph, labelDict, _, typeDict = func_get_lab_graph(modelDir, labDir, software)
        software_graph[software] = graph

    correlation_analysis_dir = os.path.join(LabSpace, '.sim.SI', 'correlation_analysis')
    if not os.path.exists(correlation_analysis_dir):
        os.makedirs(correlation_analysis_dir)

    dri_dir = os.path.join(correlation_analysis_dir, 'DRI')
    if not os.path.exists(dri_dir):
        os.makedirs(dri_dir)
        os.makedirs(os.path.join(dri_dir, "si"))
    dri_kendall_correlation_coefficient(dri_dir, software_graph)

if __name__ == '__main__':
    main()

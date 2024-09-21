import pickle
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool
from scipy.stats import kendalltau

from experiment.lab2._4_dri.config import *
from experiment.algorithms.propagation_models.sir_epidemic import sir_epidemic


epoch = 100
step = 100
beta = 0.10


def jaccard_similarity(set_a, set_b):
    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)
    return len(intersection) / len(union)


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


def get_sim_node_influence(node_influence_dir, software_name):
    node_influence_pkl = os.path.join(node_influence_dir, f"{software_name}.pkl")

    if not os.path.exists(node_influence_pkl):
        graph = Graphs[software_name]
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
        with open(node_influence_pkl, 'wb') as f:
            pickle.dump(node_influence, f)

    with open(node_influence_pkl, 'rb') as f:
        node_influence = pickle.load(f)

    return node_influence


def main(sim_threshold, epoch, step, beta):
    LoadSoftwareConfigs1()

    baseline_methods = ['DRI', 'iFit', 'Class Rank', 'Element Rank', '$GGC_d$', '$GC_d$', 'BC', 'Page Rank', 'DC']
    software_names = ['LevelDB', 'Log4cxx', 'Memcached', 'Nginx', 'Node.js', 'Redis', 'Terminal', 'VLC']

    node_influence_dir = os.path.join(LabSpace, '.sim.SI', 'node_influence', f"{epoch}-{step}-{beta}")
    if not os.path.exists(node_influence_dir):
        os.makedirs(node_influence_dir)

    result_csv = os.path.join(node_influence_dir, f'{sim_threshold}-nodes.csv')
    result_df = pd.DataFrame(columns=['method'] + baseline_methods + ['DRI rank'])

    for software_name, (status, language, src_dir) in SoftwareConfigs1.items():
        if software_name not in software_names:
            continue

        graph = Graphs[software_name]
        node_number = graph.number_of_nodes()

        if isinstance(sim_threshold, float) and 0 <= sim_threshold <= 1:
            seeds_count = int(node_number * sim_threshold)
        elif isinstance(sim_threshold, int) and 0 < sim_threshold < node_number:
            seeds_count = sim_threshold
        else:
            seeds_count = int(node_number * 0.15)

        node_influence = get_sim_node_influence(node_influence_dir, software_name)

        result_dict = dict()
        for method_name, method_dict in TestMethods:
            if method_name not in baseline_methods:
                continue

            node_data = method_dict[software_name]

            node_data = dict(sorted(node_data.items(), key=lambda item: item[1], reverse=True))
            node_ids = list(node_data.keys())
            seeds = node_ids[:seeds_count]

            si_nodes = list(node_influence.keys())[:seeds_count]

            result_dict[method_name] = round(jaccard_similarity(set(seeds), set(si_nodes)), 4)

        result_keys = list(dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True)).keys())
        result_dict['method'] = software_name
        result_dict['DRI rank'] = result_keys.index("DRI") + 1

        result_df.loc[len(result_df)] = result_dict

    result_df.to_csv(result_csv)


if __name__ == '__main__':
    for sim_threshold in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        main(sim_threshold=sim_threshold, epoch=epoch, step=step, beta=beta)

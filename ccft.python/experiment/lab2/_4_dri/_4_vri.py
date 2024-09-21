import random
import pandas as pd
from tqdm import tqdm

from experiment.lab2._4_dri.config import *
from experiment.lab2._0_config_ import SoftwareConfigs1, LabSpace
from experiment.algorithms.propagation_models.sir_epidemic import sir_epidemic

baseline_methods = ['VRI', 'sscc', 'H', 'V', 'McCabe', 'LOC']
Rounds = 100
ErrNodeRate = 0.05
beta = 0.1

LoadSoftwareConfigs1()

vulnerability_risk_identification = os.path.join(LabSpace, '.sim.SI', 'vulnerability_risk_identification')
if not os.path.exists(vulnerability_risk_identification):
    os.makedirs(vulnerability_risk_identification)

for softwareName, (status, language, src_dir) in SoftwareConfigs1.items():
    if status:
        G = Graphs[softwareName]
        types = Types[softwareName]

        df = pd.DataFrame(columns=['rate'] + baseline_methods)

        nodes = list(G.nodes)
        node_number = len(nodes)

        N = G.number_of_nodes()
        M = int(N * ErrNodeRate)

        infect_nodes = dict()
        for r in tqdm(range(Rounds), desc=f"{softwareName} SI Simulation"):
            errNodes = random.sample(nodes, M)
            siNodes, siRoundCounts, siRoundNodes = sir_epidemic(G, seeds=errNodes, beta=0.1, gamma=0.0)
            infect_nodes[r] = siNodes

        baseline_data = dict()
        for method in baseline_methods:
            data = dict(G.nodes.data(method))
            baseline_data[method] = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))  # 按照节点数据进行排序

        for ratio in range(0, 55, 5):
            node_ratio = float(ratio / 100)
            df_result = dict()
            df_result['rate'] = str(ratio) + '%'
            for method in baseline_methods:
                data = baseline_data[method]
                nodes = list(data.keys())[:int(node_number * node_ratio)]
                method_nodes = list()
                for infect in infect_nodes.values():
                    method_nodes.append(len(set(infect) & set(nodes)))
                df_result[method] = sum(method_nodes) / len(method_nodes)
            df.loc[len(df)] = df_result

        df.to_csv(os.path.join(vulnerability_risk_identification, f"{softwareName}.csv"), index=False)
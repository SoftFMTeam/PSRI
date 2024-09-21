import os

import numpy as np
import pandas as pd
from loguru import logger
from matplotlib import pyplot as plt
from networkx import DiGraph

from experiment.algorithms.propagation_models.sir_epidemic import sir_epidemic
from experiment.functions import func_SortDictByValue
from experiment.lab2._0_config_ import SoftwareConfigs1, LabSpace
from experiment.lab2._4_dri._4_graph_structure import StructuralLab
from experiment.lab2._4_dri.config import LoadSoftwareConfigs1, Steps

COLORS = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'darkgreen', 'chocolate']
LABELS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']


def main():
    LoadSoftwareConfigs1()
    DiffusivitySILab(100, 30)
    DiffusivitySILab(100, 0.05)
    # DiffusivityLab(100, 0.10)
    # DiffusivityLab(100, 0.15)
    StructuralLab(100, 30)
    StructuralLab(100, 0.05)
    # StructuralLab(100, 0.1)
    # StructuralLab(100, 0.15)
    pass


def DiffusivitySILab(sim_count, sim_threshold):
    def SI_std():
        return sir_epidemic(
            G,
            seeds=seeds,
            step=Steps,
            beta=0.1,
            gamma=0.0,
        )

    def SI_influence():
        return sir_epidemic(
            G,
            seeds=seeds,
            step=Steps,
            influence=influence
        )

    exMethods = ['DRI', 'DC', 'BC', 'Page Rank', 'Element Rank', 'Class Rank', '$GC_d$', '$GGC_d$', 'iFit']

    logger.info(f'Start SI model infection experiment,Simulated rounds:{sim_count},Threshold for testing nodes:{sim_threshold},Test method to be tested:{exMethods}')

    labDir = os.path.join(LabSpace, '.sim.SI')
    if not os.path.isdir(labDir):
        os.mkdir(labDir)

    simDir = os.path.join(labDir, f'{sim_count}-{sim_threshold}')
    if not os.path.isdir(simDir):
        os.mkdir(simDir)

    RoundsDir = os.path.join(simDir, 'Rounds')
    if not os.path.isdir(RoundsDir):
        os.mkdir(RoundsDir)

    idx = 0

    fig, axs = plt.subplots(3, 3, figsize=(18, 15))
    plt.subplots_adjust(hspace=0.3, wspace=0.22)
    for softwareName, (status, language, src_dir) in SoftwareConfigs1.items():
        if status:
            G: DiGraph = Graphs[softwareName]
            N = G.number_of_nodes()

            if isinstance(sim_threshold, float) and 0 <= sim_threshold <= 1:
                seedsCount = int(G.number_of_nodes() * sim_threshold)
            elif isinstance(sim_threshold, int) and 0 < sim_threshold < N:
                seedsCount = sim_threshold
            else:
                seedsCount = int(N * 0.15)

            logWeightDict = dict()
            maxLogWeight = 0.0
            for (u, v, datas) in G.edges(data=True):
                weight = datas['weight']
                logWeight = np.log2(weight + 1)

                logWeightDict[(u, v)] = logWeight

                maxLogWeight = max(maxLogWeight, logWeight)

            influence = dict()
            for (u, v) in logWeightDict:
                influence[(u, v)] = logWeightDict[(u, v)] / maxLogWeight / 10

            print(f'{softwareName} Start SI simulation, Initial number of nodes {seedsCount}')

            ax = axs[int(idx / 3), idx % 3]

            countDf = pd.DataFrame()

            methodsIdx = 0
            for methodName, methods in TestMethods:
                if methodName not in exMethods:
                    continue

                print(f'Method {methodName} process {sim_count} simulation')
                method = methods[softwareName]

                SortedMethod = func_SortDictByValue(method)
                SortedMethodIds = list(SortedMethod.keys())
                seeds = SortedMethodIds[:seedsCount]

                roundDF = pd.DataFrame(
                    columns=[f'round {i}' for i in range(sim_count)]
                )

                for i in range(sim_count):
                    simNodes, simRoundCounts, simRoundNodes = SI_influence()
                    # simNodes, simRoundCounts, simRoundNodes = SI_std()

                    siSimCounts = [0]
                    siSimCounts.extend(simRoundCounts)
                    roundDF[f'round {i}'] = siSimCounts

                roundDF.to_csv(os.path.join(RoundsDir, f'{softwareName}.rounds.csv'))

                resDf = roundDF.T
                countDf[methodName] = resDf.mean()
                ax.plot(countDf[methodName], label=f'{methodName}={round(max(resDf.mean()), 2)}',
                        color=COLORS[methodsIdx])

                methodsIdx += 1

            countDf.to_csv(os.path.join(simDir, f'{softwareName}.sim.csv'))

            ax.set_xlabel('Iterations', fontdict={'size': 12})
            ax.set_ylabel('Number of infected nodes', fontdict={'size': 12})
            ax.set_title(f'{LABELS[idx]}) {softwareName}', y=-0.25, fontdict={'family': 'Times New Roman', 'size': 18})
            ax.legend(loc='best')

            idx += 1
    plt.savefig(os.path.join(simDir, f'sim.png'))
    plt.show()
    pass


if __name__ == '__main__':
    main()

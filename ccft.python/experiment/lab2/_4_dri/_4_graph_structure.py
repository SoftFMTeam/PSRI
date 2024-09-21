import copy
import os

import pandas as pd
from loguru import logger

from .._0_config_ import LabSpace, SoftwareConfigs1
from .config import Graphs, TestMethods
from ...algorithms.propagation_models.sir_epidemic import sir_epidemic
from ...algorithms.utils import cal_network_efficiency, cal_network_complexity
from ...functions import func_SortDictByValue


def StructuralLab(sim_threshold, epoch, step, beta):
    exMethods = ['DRI', 'DC', 'BC', 'Page Rank', 'Element Rank', 'Class Rank', '$GC_d$', '$GGC_d$', 'iFit']

    logger.info(f'Start the experiment on changes in network properties，epoch:{epoch},sim_threshold:{sim_threshold},method:{exMethods}')

    labDir = os.path.join(LabSpace, '.sim.SI', 'network_loss')
    if not os.path.isdir(labDir):
        os.mkdir(labDir)

    simDir = os.path.join(labDir, f'{sim_threshold}-{epoch}-{step}-{beta}')
    if not os.path.isdir(simDir):
        os.mkdir(simDir)

    cols = ['name'] + exMethods

    dfEfficiency = pd.DataFrame(columns=cols)
    dfComplexity = pd.DataFrame(columns=cols)

    idx = 0
    for softwareName, (status, language, src_dir) in SoftwareConfigs1.items():
        if status:
            G = Graphs[softwareName]
            N = G.number_of_nodes()

            efficiencyDict = {
                'name': softwareName
            }
            complexityDict = {
                'name': softwareName
            }

            srcEfficiency = cal_network_efficiency(G)
            srcComplexity = cal_network_complexity(G)

            if isinstance(sim_threshold, float) and 0 <= sim_threshold <= 1:
                seedsCount = int(G.number_of_nodes() * sim_threshold)
            elif isinstance(sim_threshold, int) and 0 < sim_threshold < N:
                seedsCount = sim_threshold
            else:
                seedsCount = int(N * 0.15)

            print(f'processing software {softwareName}')
            for methodName, methods in TestMethods:
                if methodName not in exMethods:
                    continue

                method = methods[softwareName]
                SortedMethod = func_SortDictByValue(method)
                SortedMethodIds = list(SortedMethod.keys())
                seeds = SortedMethodIds[:seedsCount]
                print(f'\tprocessing software {methodName}')

                totalEfficiency = 0.0
                totalComplexity = 0.0
                for i in range(epoch):
                    simNodes, simRoundCounts, simRoundNodes = sir_epidemic(G, seeds=seeds, step=step, beta=beta,
                                                                           gamma=0.0)
                    tG = copy.deepcopy(G)
                    tG.remove_nodes_from(simNodes)
                    tEfficiency = cal_network_efficiency(tG)
                    totalEfficiency += tEfficiency
                    tComplexity = cal_network_complexity(tG)
                    totalComplexity += tComplexity
                totalEfficiency /= epoch
                totalComplexity /= epoch

                efficiencyDict[methodName] = round((srcEfficiency - totalEfficiency) / srcEfficiency, 3)
                complexityDict[methodName] = round((srcComplexity - totalComplexity) / srcComplexity, 3)

            dfEfficiency.loc[idx] = efficiencyDict
            dfComplexity.loc[idx] = complexityDict
            idx += 1
    dfEfficiency.to_csv(os.path.join(simDir, 'Efficiency.csv'))
    dfComplexity.to_csv(os.path.join(simDir, 'Complexity.csv'))

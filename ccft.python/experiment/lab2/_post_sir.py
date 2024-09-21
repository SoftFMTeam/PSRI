import math
import os
import shutil

import pandas as pd
from loguru import logger

from ccft.util.utils import deserialize
from experiment.algorithms.propagation_models.sir_epidemic import sir_epidemic
from experiment.functions import func_get_lab_graph
from experiment.lab2._0_config_ import SoftwareConfigs1, LabSpace


def main():
    simCount = 5

    for softwareName, (status, language, src_dir) in SoftwareConfigs1.items():
        if status:
            logger.info(f'===========================>>> {softwareName} Sir infectious disease model simulation')

            modelDir = os.path.join(LabSpace, softwareName)
            labDir = os.path.join(modelDir, '.lab2')
            expPath = os.path.join(labDir, 'experiments.bin')
            sirDir = os.path.join(labDir, 'sir')

            if not os.path.isdir(labDir):
                raise Exception(f'{softwareName} experiment does not exist')

            if os.path.isdir(sirDir):
                shutil.rmtree(sirDir)
            os.makedirs(sirDir)

            labGraph, labelDict, infoDict = func_get_lab_graph(modelDir, labDir, softwareName)
            logger.info(f'Load image file {labDir}')

            experiments = deserialize(expPath)
            logger.info(f'Load the experimental result file {expPath}')

            if labGraph.number_of_nodes() < 30:
                seedsCount = labGraph.number_of_nodes()
            else:
                seedsCount = math.floor(labGraph.number_of_nodes() * 0.15)
            logger.info(f'Record the top {seedsCount} nodes in all algorithms for simulation experiments')

            sim_nodes = set()
            for algName, alg_metrics in experiments.items():
                for idx in range(seedsCount):
                    sim_nodes.add(alg_metrics[0][idx])

            logger.info(f'Prepare to conduct Sir infectious disease model simulation experiment, total rounds [{simCount}]')
            for labIt in range(simCount):
                logger.info(f'Perform Sir infectious disease model simulation experiment [{labIt}]...')
                sir_results = __sir_simulate__(labGraph, sim_nodes)
                logger.info(f'Sir infectious disease model simulation experiment [{labIt}] execution completed, record results...')

                simDf = pd.DataFrame()
                simPath = os.path.join(sirDir, f'_{labIt}.csv')
                for algName, (idList, valList, labelList) in experiments.items():
                    ids = []
                    vals = []
                    names = []
                    sList = []
                    iList = []
                    rList = []
                    sumS = 0
                    sumI = 0
                    sumR = 0

                    for idx in range(seedsCount):
                        node_id = idList[idx]
                        node_val = valList[idx]
                        node_name = labelList[idx]
                        sCount, iCount, rCount = sir_results[node_id]
                        ids.append(node_id)
                        vals.append(node_val)
                        names.append(node_name)
                        sList.append(sCount)
                        iList.append(iCount)
                        rList.append(rCount)
                        sumS += sCount
                        sumI += iCount
                        sumR += rCount

                    ids.append(None)
                    vals.append(None)
                    names.append(algName)
                    sList.append(None)
                    iList.append(sumI)
                    rList.append(None)

                    simDf[f'{algName}.id'] = ids
                    simDf[f'{algName}.val'] = vals
                    simDf[f'{algName}.name'] = names
                    simDf[f'{algName}.s'] = sList
                    simDf[f'{algName}.i'] = iList
                    simDf[f'{algName}.r'] = rList

                simDf.to_csv(simPath)
                logger.info(f'The results of the Sir infectious disease model simulation experiment [{labIt}] have been recorded in {simPath} ')
    pass


def __get_algorithms_results__(measurements):
    results = dict()

    columns = measurements.columns.tolist()[1:]
    algorithms_count = int(len(columns) / 3)

    for i in range(algorithms_count):
        name = columns[3 * i][:-4]
        results[name] = (
            measurements[columns[3 * i]], measurements[columns[3 * i + 1]], measurements[columns[3 * i + 2]])

    return results


def __sir_simulate__(graph, sim_nodes):
    simulate_res = dict()

    for node_id in sim_nodes:
        sir_list = sir_epidemic(G=graph, seeds=[node_id], beta=0.15, gamma=0.0)
        if sir_list:
            (sC, iC, rC) = sir_list[-1]
        else:
            (sC, iC, rC) = (0, 0, 0)

        simulate_res[node_id] = (sC, iC, rC)

    return simulate_res


if __name__ == '__main__':
    main()

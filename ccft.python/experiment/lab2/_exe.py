import os.path

import networkx as nx
import numpy as np
import pandas as pd
from loguru import logger

from ccft.util.utils import sorted_dict_values, serialize
from experiment.algorithms.rank.anc_rank_ import alg_nac_rank0
from experiment.algorithms.rank.het_gm_rank import het_gm_rank
from experiment.algorithms.rank.page_rank_ import alg_page_rank
from experiment.functions import func_std, func_mul, func_get_lab_graph
from experiment.lab2._0_config_ import SoftwareConfigs1, LabSpace


def main():
    for softwareName, (status, language, src_dir) in SoftwareConfigs1.items():
        if status:
            logger.info(f'---------------- run {softwareName} experiment ----------------')
            modelDir = os.path.join(LabSpace, softwareName)
            labDir = os.path.join(modelDir, '.lab2')

            if not os.path.isdir(labDir):
                os.makedirs(labDir, exist_ok=True)

            logger.info(f'>>> {softwareName} >>> Read network objects')
            labGraph, labelDict, _ = func_get_lab_graph(modelDir, labDir, softwareName)

            logger.info(f'>>> {softwareName} >>> Execute the experimental process')
            experimentsDict = __experiment__(labGraph)

            logger.info(f'>>> {softwareName} >>> Save experimental results')
            dfExp = pd.DataFrame()
            experiments = dict()
            for name, result in experimentsDict.items():
                nx.set_node_attributes(labGraph, result, name)
                keys, values = sorted_dict_values(result, True)
                labels = [labelDict[i] for i in keys]
                dfExp[f'{name}_key'] = keys
                dfExp[f'{name}_val'] = values
                dfExp[f'{name}_lab'] = labels
                experiments[name] = (keys, values, labels)

            expCsvPath = f'{labDir}\\experiments.csv'
            expBinPath = f'{labDir}\\experiments.bin'
            dfExp.to_csv(expCsvPath)
            serialize(expBinPath, experiments)
            logger.info(f'The experimental results csv has been saved to {expCsvPath}')
            logger.info(f'The experimental results bin has been saved to {expBinPath}')
        pass


def power_law_func(X, a, b):
    return a * np.power(X, -b - 1)


def logarithm_func(Y, a, b):
    Y_ = Y / a
    return np.log(Y_) / np.log(-b - 1)


def __experiment__(
        G: nx.DiGraph,
):
    def __save_in_result(adict, name):
        adict_ = dict(zip(adict.keys(), adict.values()))
        results[name] = adict_
        pass

    results = dict()

    logger.info('Experimental execution')

    logger.info(f'=====> Node failure occurrence capability AFO')
    nacRank, _ = alg_nac_rank0(G)
    # __save_in_result(nacRank, 'nacRank')
    AFORank = func_std(nacRank)
    __save_in_result(AFORank, 'AFORank')
    logger.info(f'complete\n')

    logger.info(f'=====> Node Failure Propagation Capability AFP，0.15 * degree_cal + 0.85 * pre_imp')
    ImpRank, ImpFir, ImpSec = alg_page_rank(G, first_cal='degree')
    # __save_in_result(ImpRank, 'ImpRank')
    # __save_in_result(ImpFir, 'ImpFir')
    # __save_in_result(ImpSec, 'ImpSec')
    AFPRank = func_std(ImpRank)
    __save_in_result(AFPRank, 'AFPRank')
    logger.info(f'complete\n')

    logger.info(f'=====> Node risk degree AR')
    ARRank = func_mul(AFORank, AFPRank)
    __save_in_result(ARRank, 'ARRank')
    logger.info(f'complete\n')

    # logger.info(f'=====> Gm AFO*AFP，cut-off radius=3，ERR')
    # GmRankOP = het_gm_rank1(G, AFORank, AFPRank)
    # __save_in_result(GmRankOP, 'ERR GmRank=AFO*AFP')
    # logger.info(f'complete\n')

    logger.info(f'=====> Gm AFP*AFO，cut-off radius=3')
    GmRank_PO = het_gm_rank(G, AFPRank, AFORank, beta=0)
    __save_in_result(GmRank_PO, 'GmRank=AFP*AFO')
    logger.info(f'complete\n')

    logger.info(f'=====> Gm AR*AR，cut-off radius=3')
    GmRank_AR = het_gm_rank(G, ARRank, ARRank, beta=0)
    __save_in_result(GmRank_AR, 'GmRank=AR*AR')
    logger.info(f'complete\n')

    logger.info(f'=====> DC')
    dc = nx.degree_centrality(G)
    __save_in_result(dc, 'DC')
    logger.info(f'complete\n')

    logger.info(f'=====> BC')
    bc = nx.betweenness_centrality(G)
    __save_in_result(bc, 'BC')
    logger.info(f'complete\n')

    return results


if __name__ == '__main__':
    main()

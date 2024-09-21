import collections
import os.path

import networkx as nx
import numpy as np
import pandas as pd
from loguru import logger
from matplotlib import pyplot as plt

from ccft.util.utils import sorted_dict_values, deserialize, serialize, sorted_dict_keys
from experiment.algorithms.distribution.powerlaw_ana import powerlaw_fit
from experiment.algorithms.rank.anc_rank_ import alg_nac_rank0
from experiment.algorithms.rank.het_gm_rank import het_gm_rank
from experiment.algorithms.rank.page_rank_ import alg_page_rank
from experiment.functions import func_get_lab_graph, func_std, func_mul
from experiment.lab2._0_config_ import SoftwareConfigs1, LabSpace


def main():
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    logger.info(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Network Structure Analysis >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    sumMeasureDir = os.path.join(LabSpace, '.measure')
    # if os.path.isdir(sumMeasureDir):
    #     shutil.rmtree(sumMeasureDir)
    # os.mkdir(sumMeasureDir)

    degreeDir = os.path.join(sumMeasureDir, 'degree')
    # os.makedirs(degreeDir)
    inDegreeDir = os.path.join(sumMeasureDir, 'in-degree')
    # os.makedirs(inDegreeDir)
    outDegreeDir = os.path.join(sumMeasureDir, 'out-degree')
    # os.makedirs(outDegreeDir)
    bcDir = os.path.join(sumMeasureDir, 'bc')
    # os.makedirs(bcDir)
    clusteringDir = os.path.join(sumMeasureDir, 'clustering')
    # os.makedirs(clusteringDir)
    AFODir = os.path.join(sumMeasureDir, 'AFO')
    # os.makedirs(AFODir)
    AFPDir = os.path.join(sumMeasureDir, 'AFP')
    # os.makedirs(AFPDir)
    ARDir = os.path.join(sumMeasureDir, 'AR')
    # os.makedirs(ARDir)
    GMPDir = os.path.join(sumMeasureDir, 'GMP')
    # os.makedirs(GMPDir)
    GMSDir = os.path.join(sumMeasureDir, 'GMS')
    # os.makedirs(GMSDir)

    degreePlInfo = pd.DataFrame(columns=['Name', 'alpha', 'sigma', 'xMin', 'pBeta', 'D'])
    inDegreePlInfo = pd.DataFrame(columns=['Name', 'alpha', 'sigma', 'xMin', 'pBeta', 'D'])
    outDegreePlInfo = pd.DataFrame(columns=['Name', 'alpha', 'sigma', 'xMin', 'pBeta', 'D'])

    measurements = {
        'degree': dict(),
        'in-degree': dict(),
        'out-degree': dict(),
        'bc': dict(),
        'clustering': dict(),
        'AFO': dict(),
        'AFP': dict(),
        'AR': dict(),
        'GMP': dict(),
        'GMS': dict(),
    }

    loc = 0
    for softwareName, (status, language, src_dir) in SoftwareConfigs1.items():
        if status:
            modelDir = os.path.join(LabSpace, softwareName)
            labDir = os.path.join(modelDir, '.lab2')

            if not os.path.isdir(labDir):
                os.makedirs(labDir, exist_ok=True)

            logger.info(
                f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {softwareName} Read network objects >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            G, labelDict, _, typeDict = func_get_lab_graph(modelDir, labDir, softwareName)

            logger.debug(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {softwareName} Degree distribution >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            degDict = dict(G.degree())
            degrees = np.asarray(list(degDict.values()))
            degreeIds = np.asarray(list(degDict.keys()))
            degreeLabs = np.asarray([labelDict[i] for i in degreeIds])
            degreeTypes = np.asarray([typeDict[i] for i in degreeIds])
            np.savetxt(os.path.join(degreeDir, f'{softwareName}.csv'), degrees)
            measurements['degree'][softwareName] = (degrees, degreeIds, degreeLabs)
            powerlaw_ana(degrees, softwareName, degreePlInfo, loc, False)
            df = pd.DataFrame()
            df['value'] = degrees
            df['id'] = degreeIds
            df['lab'] = degreeLabs
            df['type'] = degreeTypes
            df.to_csv(os.path.join(degreeDir, f'{softwareName}-all.csv'))

            logger.debug(
                f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {softwareName} in-degree distribution >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            inDegDict = dict(G.in_degree())
            inDegrees = np.asarray(list(inDegDict.values()))
            inDegreeIds = np.asarray(list(inDegDict.keys()))
            inDegreeLabs = np.asarray([labelDict[i] for i in inDegreeIds])
            inDegreeTypes = np.asarray([typeDict[i] for i in inDegreeIds])
            np.savetxt(os.path.join(inDegreeDir, f'{softwareName}.csv'), inDegrees)
            measurements['in-degree'][softwareName] = (inDegrees, inDegreeIds, inDegreeLabs)
            powerlaw_ana(inDegrees, softwareName, inDegreePlInfo, loc, bi=1)
            df = pd.DataFrame()
            df['value'] = inDegrees
            df['id'] = inDegreeIds
            df['lab'] = inDegreeLabs
            df['type'] = inDegreeTypes
            df.to_csv(os.path.join(inDegreeDir, f'{softwareName}-all.csv'))

            logger.debug(
                f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {softwareName} Degree distribution >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            outDegDict = dict(G.out_degree())
            outDegrees = np.asarray(list(outDegDict.values()))
            outDegreeIds = np.asarray(list(outDegDict.keys()))
            outDegreeLabs = np.asarray([labelDict[i] for i in outDegreeIds])
            outDegreeTypes = np.asarray([typeDict[i] for i in outDegreeIds])
            np.savetxt(os.path.join(outDegreeDir, f'{softwareName}.csv'), outDegrees)
            measurements['out-degree'][softwareName] = (outDegrees, outDegreeIds, outDegreeLabs)
            powerlaw_ana(outDegrees, softwareName, outDegreePlInfo, loc, bi=1)
            df = pd.DataFrame()
            df['value'] = outDegrees
            df['id'] = outDegreeIds
            df['lab'] = outDegreeLabs
            df['type'] = outDegreeTypes
            df.to_csv(os.path.join(outDegreeDir, f'{softwareName}-all.csv'))

            logger.debug(
                f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {softwareName} Median distribution >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            bcDict = dict(nx.betweenness_centrality(G, normalized=False))
            bcs = np.asarray(list(bcDict.values()))
            bcIds = np.asarray(list(bcDict.keys()))
            bcLabs = np.asarray([labelDict[i] for i in bcIds])
            measurements['bc'][softwareName] = (bcs, bcIds, bcLabs)
            np.savetxt(os.path.join(bcDir, f'{softwareName}.csv'), bcs)

            logger.debug(
                f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {softwareName} Agglomeration coefficient distribution >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            clusDict = dict(nx.clustering(G))
            clus = np.asarray(list(clusDict.values()))
            cluIds = np.asarray(list(clusDict.keys()))
            cluLabs = np.asarray([labelDict[i] for i in cluIds])
            measurements['clustering'][softwareName] = (clus, cluIds, cluLabs)
            np.savetxt(os.path.join(clusteringDir, f'{softwareName}.csv'), clus)

            logger.debug(
                f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {softwareName} Node failure occurrence capability AFO >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            nacRank, _ = alg_nac_rank0(G)
            afos = func_std(nacRank)
            afoVals = np.asarray(list(afos.values()))
            afoIds = np.asarray(list(afos.keys()))
            afoLabs = np.asarray([labelDict[i] for i in afoIds])
            measurements['AFO'][softwareName] = (afoVals, afoIds, afoLabs)
            np.savetxt(os.path.join(AFODir, f'{softwareName}.csv'), afoVals)

            logger.debug(
                f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {softwareName} Node Failure Propagation Capability AFP >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            ImpRank, ImpFir, ImpSec = alg_page_rank(G, first_cal='degree')
            afps = func_std(ImpRank)
            afpVals = np.asarray(list(afps.values()))
            afpIds = np.asarray(list(afps.keys()))
            afpLabs = np.asarray([labelDict[i] for i in afpIds])
            measurements['AFP'][softwareName] = (afpVals, afpIds, afpLabs)
            np.savetxt(os.path.join(AFPDir, f'{softwareName}.csv'), afpVals)

            logger.debug(
                f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {softwareName} AR=AFP*AFO >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            ars = func_mul(afos, afps)
            arVals = np.asarray(list(ars.values()))
            arIds = np.asarray(list(ars.keys()))
            arLabs = np.asarray([labelDict[i] for i in arIds])
            measurements['AR'][softwareName] = (arVals, arIds, arLabs)
            np.savetxt(os.path.join(ARDir, f'{softwareName}.csv'), arVals)

            logger.debug(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {softwareName} GMP >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            gmps = het_gm_rank(G, afos, afps, alpha=1, beta=0)
            gmpVals = np.asarray(list(gmps.values()))
            gmpIds = np.asarray(list(gmps.keys()))
            gmpLabs = np.asarray([labelDict[i] for i in gmpIds])
            measurements['GMP'][softwareName] = (gmpVals, gmpIds, gmpLabs)
            np.savetxt(os.path.join(GMPDir, f'{softwareName}.csv'), gmpVals)

            logger.debug(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {softwareName} GMS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            gmss = het_gm_rank(G, afos, afps, alpha=0, beta=1)
            gmsVals = np.asarray(list(gmss.values()))
            gmsIds = np.asarray(list(gmss.keys()))
            gmsLabs = np.asarray([labelDict[i] for i in gmsIds])
            measurements['GMP'][softwareName] = (gmsVals, gmsIds, gmsLabs)
            np.savetxt(os.path.join(GMSDir, f'{softwareName}.csv'), gmsVals)

            loc += 1
            pass

    degreePlInfo.to_csv(os.path.join(sumMeasureDir, 'degree', '.powerlaw.deg.csv'))
    inDegreePlInfo.to_csv(os.path.join(sumMeasureDir, 'in-degree', '.powerlaw.in-deg.csv'))
    outDegreePlInfo.to_csv(os.path.join(sumMeasureDir, 'out-degree', '.powerlaw.out-deg.csv'))
    serialize(os.path.join(sumMeasureDir, '.measurements.bin'), measurements)


def powerlaw_ana(seqs, softwareName, infoDict, loc, visual=False, bi=0):
    fit, info, X, Y, logX, logY = powerlaw_fit(seqs, plotPdf=visual, bi=bi, kMinPlot=False,
                                               title=f'{softwareName} Degree distribution')
    info['Name'] = softwareName
    infoDict.loc[loc] = info

    logger.warning(f'Power law distribution parameters alpha={fit.alpha}, sigma={fit.sigma}, xMin={fit.xmin}, D={fit.D}')
    R, p = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    logger.warning(f'Power law distribution vs exponential distribution  loglikelihood ratio={R}, p-value={p}')
    R, p = fit.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
    logger.warning(f'Power law distribution vs Lognormal: loglikelihood ratio R={R}, p-value={p}')

    pass


def __measurement__(softwareName, G, measureBinPath, labelDict, reload=False):
    if reload or not os.path.isfile(measureBinPath):
        def __save__(adict, meaName, keyLabel='id', valLabel='value', useLabel=True, sortValue=True):
            df = pd.DataFrame()
            if sortValue:
                meaKeys, meaValues = sorted_dict_values(adict, True)
            else:
                meaKeys, meaValues = sorted_dict_keys(adict, True)

            df[keyLabel] = meaKeys
            df[valLabel] = meaValues

            if useLabel:
                labels = [labelDict[i] for i in meaKeys]
                df[f'label'] = labels
            else:
                count = len(adict)
                if count < 5:
                    logger.error(f'The number of path distributions [{count}] for {softwareName} is too low')

            results[meaName] = df
            pass

        def _dfs_(n, pathLen, visited):
            if pathLen in pathDict:
                pathDict[pathLen] += 1
            else:
                pathDict[pathLen] = 1

            if n not in visited:
                visited.add(n)

                for succ in G.successors(n):
                    _dfs_(succ, pathLen + 1, visited)

        results = dict()

        Deg = dict(G.degree())
        __save__(Deg, 'degree')
        degValues = results['degree']['value']
        degCounter = collections.Counter(degValues)
        __save__(degCounter, 'degree-counter', 'degree', 'count', useLabel=False, sortValue=False)

        InDeg = dict(G.in_degree())
        __save__(InDeg, 'in-degree')
        inDegValues = results['in-degree']['value']
        inDegCounter = collections.Counter(inDegValues)
        __save__(inDegCounter, 'in-degree-counter', 'in-degree', 'count', useLabel=False, sortValue=False)

        OutDeg = dict(G.out_degree())
        __save__(OutDeg, 'out-degree')
        outDegValues = results['out-degree']['value']
        outDegCounter = collections.Counter(outDegValues)
        __save__(outDegCounter, 'out-degree-counter', 'out-degree', 'count', useLabel=False, sortValue=False)

        bc = nx.betweenness_centrality(G, normalized=False)
        __save__(bc, 'betweenness')

        clustering = nx.clustering(G)
        __save__(clustering, 'clustering')

        pathDict = dict()
        for node in G.nodes:
            _dfs_(node, 0, set())
        __save__(pathDict, 'path', useLabel=False)

        serialize(measureBinPath, results)
        logger.info(f'The measurement results have been saved to a file {measureBinPath}')
    else:
        logger.info('Load measurement results')
        results = deserialize(measureBinPath)

    return results


if __name__ == '__main__':
    main()

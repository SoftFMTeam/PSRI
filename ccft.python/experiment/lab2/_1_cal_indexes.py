import os

import networkx as nx
from loguru import logger

from experiment.algorithms.rank.anc_rank_ import alg_nac_rank0
from experiment.algorithms.rank.element_rank import element_rank, pr_rank
from experiment.algorithms.rank.het_gm_rank import het_gm_rank, gc_rank, ggc_rank, gcd_rank, ggcd_rank, iFit_rank
from experiment.algorithms.rank.page_rank_ import alg_page_rank
from experiment.functions import func_get_lab_graph, func_std, save_graph
from experiment.lab2._0_config_ import SoftwareConfigs1, SoftwareConfigs2, LabSpace

ReCal = False


def cal_method_indexes():
    SoftwareConfigs = dict()
    for key, val in SoftwareConfigs1.items():
        SoftwareConfigs[key] = val
    for key, val in SoftwareConfigs2.items():
        SoftwareConfigs[key] = val
    for softwareName, (status, language, src_dir) in SoftwareConfigs.items():
        if status:
            modelDir = os.path.join(LabSpace, softwareName)
            labDir = os.path.join(modelDir, '.lab2')
            logger.info(f'{softwareName} starts calculating experimental indicators')

            G, labelDict, _, typeDict = func_get_lab_graph(modelDir, labDir, softwareName)

            nacRank, _ = alg_nac_rank0(G)
            AFORank = func_std(nacRank)
            AFOList = [(key, {'AFO': val}) for key, val in AFORank.items()]
            G.add_nodes_from(AFOList)
            logger.debug('Node failure occurrence capability AFO calculation completed')

            ImpRank, ImpFir, ImpSec = alg_page_rank(G, first_cal='degree')
            AFPRank = func_std(ImpRank)
            AFPList = [(key, {'AFP': val}) for key, val in AFPRank.items()]
            G.add_nodes_from(AFPList)
            logger.debug('Node failure propagation capability AFP calculation completed')

            VRI = het_gm_rank(G, AFORank, AFPRank, alpha=0)
            VRIList = [(key, {'VRI': val}) for key, val in VRI.items()]
            G.add_nodes_from(VRIList)
            logger.debug('Node risk vulnerability index VRI calculation completed')

            DRI = het_gm_rank(G, AFORank, AFPRank, beta=0)
            DRIList = [(key, {'DRI': val}) for key, val in DRI.items()]
            G.add_nodes_from(DRIList)
            logger.debug('Node risk diffusion index DRI calculation completed')

            VMulD = [(node, {'VMulD': (data['VRI'] + 1) * (data['DRI'] + 1)}) for node, data in
                     G.nodes(data=True)]
            G.add_nodes_from(VMulD)
            logger.debug('(VRI+1) * (DRI+1) Calculation completed')

            VPlusD = [(node, {'VPlusD': (data['VRI'] + data['DRI'])}) for node, data in G.nodes(data=True)]
            G.add_nodes_from(VPlusD)
            logger.debug('VRI+DRI calculation completed')

            save_graph(labDir, G)
            logger.info('Calculation completed, results saved to', labDir)
    pass


def cal_indexes():
    SoftwareConfigs = dict()
    for key, val in SoftwareConfigs1.items():
        SoftwareConfigs[key] = val
    for key, val in SoftwareConfigs2.items():
        SoftwareConfigs[key] = val
    for softwareName, (status, language, src_dir) in SoftwareConfigs.items():
        if status:
            modelDir = os.path.join(LabSpace, softwareName)
            labDir = os.path.join(modelDir, '.lab2')
            logger.info(f'{softwareName} Start calculating comparison method indicators...')

            G, labelDict, _, typeDict = func_get_lab_graph(modelDir, labDir, softwareName)

            for _, data in G.nodes(data=True):
                if ReCal or 'dc' not in data:
                    dc = nx.degree_centrality(G)
                    dcList = [(key, {'dc': val}) for key, val in dc.items()]
                    G.add_nodes_from(dcList)
                logger.debug('Degree centrality calculation completed')

                if ReCal or 'cc' not in data:
                    cc = nx.closeness_centrality(G)
                    ccList = [(key, {'cc': val}) for key, val in cc.items()]
                    G.add_nodes_from(ccList)
                logger.debug('Close centrality calculation completed')

                if ReCal or 'bc' not in data:
                    bc = nx.betweenness_centrality(G)
                    bcList = [(key, {'bc': val}) for key, val in bc.items()]
                    G.add_nodes_from(bcList)
                logger.debug('Median centrality calculation completed')

                if ReCal or 'pg' not in data:
                    pg = nx.pagerank(G)
                    pgList = [(key, {'pg': val}) for key, val in pg.items()]
                    G.add_nodes_from(pgList)
                logger.debug('Page Rank calculation completed')

                if ReCal or 'er' not in data:
                    er = element_rank(G)
                    erList = [(key, {'er': val}) for key, val in er.items()]
                    G.add_nodes_from(erList)
                logger.debug('Element Rank calculation completed')

                if ReCal or 'cr' not in data:
                    CrRank, CrFir, CrSec = alg_page_rank(G, first_cal='weight_degree')
                    CRRank = func_std(CrRank)
                    CRList = [(key, {'cr': val}) for key, val in CRRank.items()]
                    G.add_nodes_from(CRList)
                logger.debug('Class Rank calculation completed')

                if ReCal or 'gc' not in data:
                    gc = gc_rank(G)
                    gcList = [(key, {'gc': val}) for key, val in gc.items()]
                    G.add_nodes_from(gcList)
                logger.debug('The calculation of the center of gravity has been completed')

                if ReCal or 'ggc' not in data:
                    ggc = ggc_rank(G)
                    ggcList = [(key, {'ggc': val}) for key, val in ggc.items()]
                    G.add_nodes_from(ggcList)
                logger.debug('GGC calculation completed')

                if ReCal or 'gcd' not in data:
                    gcd = gcd_rank(G)
                    gcdList = [(key, {'gcd': val}) for key, val in gcd.items()]
                    G.add_nodes_from(gcdList)
                logger.debug('The calculation of the center of gravity has been completed')

                if ReCal or 'ggcd' not in data:
                    ggcd = ggcd_rank(G)
                    ggcdList = [(key, {'ggcd': val}) for key, val in ggcd.items()]
                    G.add_nodes_from(ggcdList)
                logger.debug('GGC calculation completed')

                if ReCal or 'iFit' not in data:
                    pr = pr_rank(G)
                    iFit = iFit_rank(G, pr)
                    iFitList = [(key, {'iFit': val}) for key, val in iFit.items()]
                    G.add_nodes_from(iFitList)
                logger.debug('IFit calculation completed')

                break
            save_graph(labDir, G)
            logger.info('Calculation completed, results saved to', labDir)
    pass


if __name__ == '__main__':
    # cal_method_indexes()
    cal_indexes()

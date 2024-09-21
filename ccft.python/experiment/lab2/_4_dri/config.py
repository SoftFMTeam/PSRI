import os

from loguru import logger

from experiment.functions import func_get_lab_graph
from experiment.lab2._0_config_ import LabSpace, SoftwareConfigs1


Graphs = dict()
Labels = dict()
Types = dict()

DRIs = dict()
VRIs = dict()
VPlusDs = dict()
VMulDs = dict()
DCs = dict()
BCs = dict()
CCs = dict()
PGs = dict()
ERs = dict()
CRs = dict()
GCs = dict()
GCDs = dict()
GGCs = dict()
GGCDs = dict()
iFits = dict()

AFOs = dict()
AFPs = dict()


TestMethods = [
    ('DRI', DRIs),
    ('VRI', VRIs),
    ('DC', DCs),
    ('BC', BCs),
    ('VPlusD', VPlusDs),
    ('VMulD', VMulDs),
    ('CC', CCs),
    ('Page Rank', PGs),
    ('Element Rank', ERs),
    ('Class Rank', CRs),
    ('GC', GCs),
    ('$GC_d$', GCDs),
    ('GGC', GGCs),
    ('$GGC_d$', GGCDs),
    ('iFit', iFits),
]

Steps = 100


def LoadSoftwareConfigs1():
    logger.info('Extract experimental data for use [SoftwareConfigs1] ...')
    for softwareName, (status, language, src_dir) in SoftwareConfigs1.items():
        if status:
            modelDir = os.path.join(LabSpace, softwareName)
            labDir = os.path.join(modelDir, '.lab2')

            if not os.path.isdir(labDir):
                os.makedirs(labDir, exist_ok=True)

            G, labelDict, _, typeDict = func_get_lab_graph(modelDir, labDir, softwareName)

            Graphs[softwareName] = G
            Labels[softwareName] = labelDict
            Types[softwareName] = typeDict

            DRIs[softwareName] = dict(G.nodes.data('DRI'))
            VRIs[softwareName] = dict(G.nodes.data('VRI'))
            AFOs[softwareName] = dict(G.nodes.data('AFO'))
            AFPs[softwareName] = dict(G.nodes.data('AFP'))
            VPlusDs[softwareName] = dict(G.nodes.data('VPlusD'))
            VMulDs[softwareName] = dict(G.nodes.data('VMulD'))

            DCs[softwareName] = dict(G.nodes.data('dc'))
            BCs[softwareName] = dict(G.nodes.data('bc'))
            CCs[softwareName] = dict(G.nodes.data('cc'))
            PGs[softwareName] = dict(G.nodes.data('pg'))
            ERs[softwareName] = dict(G.nodes.data('er'))
            CRs[softwareName] = dict(G.nodes.data('cr'))
            GCs[softwareName] = dict(G.nodes.data('gc'))
            GCDs[softwareName] = dict(G.nodes.data('gcd'))
            GGCs[softwareName] = dict(G.nodes.data('ggc'))
            GGCDs[softwareName] = dict(G.nodes.data('ggcd'))
            iFits[softwareName] = dict(G.nodes.data('iFit'))

    pass

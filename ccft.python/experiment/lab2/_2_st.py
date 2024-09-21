import numpy as np
import pandas as pd
from experiment.lab2._4_dri.config import *
from experiment.lab2.lab2_func import get_pdf
from experiment.lab2._0_config_ import SoftwareConfigs1, LabSpace

LoadSoftwareConfigs1()

InfoDir = os.path.join(LabSpace, '.st')
if not os.path.isdir(InfoDir):
    os.makedirs(InfoDir, exist_ok=True)

columns = ['k', 'LevelDB', 'Log4cxx', 'Memcached', 'Nginx', 'Node.js', 'Opencv', 'Redis', 'Terminal', 'VLC']

df_all = list()

for softwareName, (status, language, src_dir) in SoftwareConfigs1.items():
    if status:
        G = Graphs[softwareName]
        degrees = dict(G.degree())
        outDegreeVals = np.asarray(list(degrees.values()))
        k, Pk = get_pdf(outDegreeVals)

        df = pd.DataFrame(columns=['k', softwareName])
        df['k'] = k
        df[softwareName] = Pk

        df_all.append(df)

# result_df = pd.concat(df_all, axis=1)

result_df = pd.DataFrame(columns=['k'])
for df in df_all:
    result_df = pd.merge(result_df, df, on='k', how='outer')

result_df.to_csv(os.path.join(InfoDir, 'degree distribution.csv'), index=False)
import os

import numpy as np
import pandas as pd
from loguru import logger
from matplotlib import pyplot as plt

from ccft.util.utils import deserialize
from experiment.lab2._0_config_ import SoftwareConfigs1, LabSpace

algNameMap = {
    'degree': 'degree',
    'in-degree': 'in-degree',
    'out-degree': 'out-degree',
    'path': 'path',
    'betweenness': 'betweenness',
    'clustering': 'clustering',
}


def main():
    measureDict = dict()

    algNames = set()
    for softwareName, (status, language, src_dir) in SoftwareConfigs1.items():
        if status:
            modelDir = os.path.join(LabSpace, softwareName)
            labDir = os.path.join(modelDir, '.lab2')
            measureDir = os.path.join(labDir, 'measure')
            measurePath = os.path.join(measureDir, 'measurements.bin')

            logger.info('Load measurement results')
            measurements = deserialize(measurePath)
            for algName in measurements:
                algNames.add(algName)
            measureDict[softwareName] = measurements

    degree_view(measureDict)
    pass


def degree_view(measureDict):
    logger.info(f'Draw the distribution of systems')
    idx = 0
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(30, 30))
    for softwareName, measurements in measureDict.items():
        logger.info(f'===>>> {softwareName}')
        col = int(idx / 3)
        row = idx % 3
        ax = axes[col, row]
        idx += 1

        values = measurements['degree'][1]
        series = pd.Series(np.log(values))

        analysis = series.describe()
        logger.info(f'Degree distribution information {analysis}')

        unique_values_count = series.nunique()
        logger.info(f"Unique values: {unique_values_count}")

        series.hist(ax=ax, bins=range(series.min(), series.max()+2))
        ax.set_xlabel(softwareName)
        ax.set_ylabel('count')
    fig.show()
    pass



def view(seq, title, ):
    plt.figure(figsize=(10, 6))
    plt.hist(seq, bins=range(max(seq) + 2), align='left')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.title('Degree Distribution of the Network')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()

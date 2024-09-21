import os
import shutil

from loguru import logger

from experiment.lab2._0_config_ import SoftwareConfigs1, LabSpace


def main():
    for softwareName, (status, language, src_dir) in SoftwareConfigs1.items():
        if status:
            logger.info(f'Clear {softwareName} experimental data')
            modelDir = os.path.join(LabSpace, softwareName)
            labDir = os.path.join(modelDir, '.lab2')
            # labDir = os.path.join(modelDir)
            if os.path.isdir(labDir):
                shutil.rmtree(labDir)
                logger.info(f'The experimental data folder {labDir} has been cleared')
            else:
                logger.warning(f'The experimental data folder {labDir} does not exist')


if __name__ == '__main__':
    main()

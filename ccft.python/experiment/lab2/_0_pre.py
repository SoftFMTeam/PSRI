import os
import shutil
import subprocess

import pandas as pd
from loguru import logger

from ccft.util.utils import serialize
from experiment.functions import func_get_lab_graph
from experiment.lab2._0_config_ import SoftwareConfigs1, LabSpace, JoernCliDir, SoftwareConfigs2


def main():
    logger.info(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Pre-Experiment >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    copy_to = os.path.join(LabSpace, 'CopyTo.exe')

    softwareInfos = pd.DataFrame(
        columns=[
            'Name', 'File', 'LOC', 'TypeDecl', 'Method', 'Local', 'Property', 'Variable',
            'Basic-Node', 'Basic-Edge', 'Topic-Node', 'Topic-Edge', 'Lab-Node', 'Lab-Edge'
        ]
    )

    loc = 0

    SoftwareConfigs = dict()
    for key, val in SoftwareConfigs1.items():
        SoftwareConfigs[key] = val
    for key, val in SoftwareConfigs2.items():
        SoftwareConfigs[key] = val

    for softwareName, (status, language, src_dir) in SoftwareConfigs.items():
        if status:
            logger.info(f'---------------- {softwareName} ----------------')

            logger.info(f'>>> {softwareName} >>> Generate CPG file')
            __gen_cpg__(softwareName, language, src_dir, LabSpace, JoernCliDir, copy_to)

            logger.info(f'>>> {softwareName} >>> Generate experimental network')
            modelDir = os.path.join(LabSpace, softwareName)
            labDir = os.path.join(modelDir, '.lab2')

            labGraph, _, softwareInfo, _ = func_get_lab_graph(modelDir, labDir, softwareName, False)

            softwareInfo['Name'] = softwareName
            softwareInfos.loc[loc] = softwareInfo
            loc += 1

    serialize(os.path.join(LabSpace, 'dataset.bin'), softwareInfos)
    softwareInfos.to_csv(os.path.join(LabSpace, 'dataset.csv'))
    pass


def __gen_cpg__(
        software_name: str,
        language: str,
        src_dir: str,
        lab_space: str,
        joern_cli_dir: str,
        copy_to: str
):
    c2cpg = os.path.join(joern_cli_dir, 'c2cpg.bat')
    joern_export = os.path.join(joern_cli_dir, 'joern-export.bat')
    joern_parse = os.path.join(joern_cli_dir, 'joern-parse.bat')

    lab_dir = os.path.join(lab_space, software_name)
    code_dir = os.path.join(lab_dir, '.src')
    cpg_path = os.path.join(lab_dir, 'cpg.bin')
    odb_path = os.path.join(lab_dir, 'c.odb')
    neo4j_dir = os.path.join(lab_dir, '.neo4jcsv')

    # copy src dir to code dir
    if not os.path.isdir(code_dir):
        commands = f'{copy_to} -s {src_dir} -d {code_dir} -l {language}'
        subprocess.call(commands)

    # gen c.obd
    # if not os.path.isfile(odb_path):
    #     commands = f'{c2cpg} {src_dir} -o {odb_path} -J-Xmx36G'
    #     subprocess.call(commands)

    # gen cpg.bin
    if not os.path.isfile(cpg_path):
        commands = f'{joern_parse} {code_dir} -o {cpg_path}  --language newc -J-Xmx48G'
        subprocess.call(commands)
        shutil.rmtree(neo4j_dir, ignore_errors=True)

    # export neo4jcsv dir
    if not os.path.isdir(neo4j_dir):
        commands = f'{joern_export} {cpg_path} --repr=all --format=neo4jcsv --out={neo4j_dir} -J-Xmx48G'
        subprocess.call(commands)
    pass


if __name__ == '__main__':
    main()

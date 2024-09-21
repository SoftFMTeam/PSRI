import os

import networkx

from ccft.helper.neo4jcsv.neo4jcsv_extra_nodes import Neo4JCsvExtraNodes
from ccft.helper.neo4jcsv.neo4jcsv_link_methods import Neo4JCsvLinkMethods
from ccft.helper.neo4jcsv.neo4jcsv_reader import Neo4jCsvReader
from ccft.helper.network_index import NetworkxIndex
from ccft.util.exceptions.error_code import ErrorCode
from ccft.util.exceptions.exception import CustomException


def neo4jcsv_read(neo4jcsv_dir):
    if neo4jcsv_dir is None or not os.path.isdir(neo4jcsv_dir):
        raise CustomException(ErrorCode.Dir_NotFound, f'neo4jcsv path \'{neo4jcsv_dir}\' not found')

    reader = Neo4jCsvReader(neo4jcsv_dir)

    return reader


def neo4jcsv_gen_networkx(reader) -> tuple[networkx.MultiDiGraph, NetworkxIndex]:
    index = NetworkxIndex()
    graph = networkx.MultiDiGraph()

    Neo4JCsvExtraNodes(reader, index, graph)
    Neo4JCsvLinkMethods(reader, index, graph)

    return graph, index

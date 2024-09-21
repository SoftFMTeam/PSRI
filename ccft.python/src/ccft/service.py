import os.path
import shutil
import subprocess

import networkx as nx
from loguru import logger
from networkx import DiGraph, MultiDiGraph

from ccft.algorithms.alg_multi_to_single import multi_to_single
from ccft.algorithms.alg_path import networkx_all_paths, networkx_shortest_path
from ccft.algorithms.alg_slice import network_slice
from ccft.algorithms.alg_subgraph import networkx_subgraph
from ccft.algorithms.alg_tree import networkx_tree
from ccft.core.constant import ENode, ERelation, EExpand
from ccft.helper.neo4jcsv.neo4jcsv_worker import neo4jcsv_gen_networkx, neo4jcsv_read
from ccft.helper.network_index import NetworkxIndex
from ccft.helper.network_worker import network_save_graph_structure
from ccft.util.exceptions.error_code import ErrorCode
from ccft.util.exceptions.exception import CustomException
from ccft.util.utils import deserialize, serialize_in_dir


def service_parse_src(
        src_dir,
        cpg_path,
        neo4jcsv_dir,
        joern_parse,
        joern_export,
):
    if not os.path.isfile(joern_parse):
        raise CustomException(ErrorCode.File_NotFound, f'Analyze script files \'{joern_parse}\' absent')

    if not os.path.isfile(joern_export):
            raise CustomException(ErrorCode.File_NotFound, f'Export script file \'{joern_export}\' absent')

    if not os.path.isdir(src_dir):
        raise CustomException(ErrorCode.Dir_NotFound, f'Source folder \'{src_dir}\' absent')

    cpg_dir = os.path.dirname(cpg_path)
    if not os.path.isdir(os.path.dirname(cpg_path)):
        os.makedirs(cpg_dir)

    # gen cpg.bin
    commands = f'{joern_parse} {src_dir} -o {cpg_path}'
    subprocess.call(commands)
    logger.info('Generate CPG: [{}]', cpg_path)

    # export neo4jcsv dir
    shutil.rmtree(neo4jcsv_dir, ignore_errors=True)
    commands = f'{joern_export} {cpg_path} --repr=all --format=neo4jcsv --out={neo4jcsv_dir}'
    subprocess.call(commands)
    logger.info('Generate neo4jcsv: [{}]', neo4jcsv_dir)
    pass


def service_parse_cpg(
        model_dir,
        neo4jcsv_dir,
):
    if not os.path.isdir(model_dir):
        os.makedirs(model_dir)

    if not os.path.isdir(neo4jcsv_dir):
        raise CustomException(ErrorCode.Dir_NotFound, f'CPG folder \'{neo4jcsv_dir}\' absent')

    graph_dict = dict()

    reader = neo4jcsv_read(neo4jcsv_dir)
    logger.info('Read CPG file completed')

    logger.info('Start parsing CPG files')
    basic_graph, index = neo4jcsv_gen_networkx(reader)

    __service_save_network_index__(model_dir, index)
    logger.info('The graph index has been saved to[{}]', os.path.join(model_dir, 'index.bin'))

    __service_save_graph__(model_dir, 'basic', basic_graph)
    graph_dict['basic'] = basic_graph
    logger.info('The graph model [basic] has been saved to [{}]', os.path.join(model_dir, 'basic'))

    topic_graph = service_cut(basic_graph, index)
    __service_save_graph__(model_dir, 'topic', topic_graph)
    graph_dict['topic'] = topic_graph
    logger.info('The graph model [topic] has been saved to [{}]', os.path.join(model_dir, 'topic'))

    return graph_dict, index


def service_load_graph(
        directory: str,
        graph_dict: dict,
        index: bool = True
):
    if directory is None:
        raise CustomException(ErrorCode.Command_Error, f'The address of the graph model cannot be empty')

    if not os.path.isdir(directory):
        raise CustomException(ErrorCode.Dir_NotFound, f'Graph model address \'{directory}\' absent')

    del_models = []
    for model_name in graph_dict.keys():
        model_dir = os.path.join(directory, model_name)
        if not os.path.isdir(model_dir):
            del_models.append(model_name)
    for model_name in del_models:
        graph_dict.pop(model_name)

    models = os.listdir(directory)
    for model_name in models:
        sub_model_dir = os.path.join(directory, model_name)
        if not model_name.startswith(".") and os.path.isdir(sub_model_dir) and model_name not in graph_dict:
            try:
                graph_path = os.path.join(sub_model_dir, 'graph.bin')
                if os.path.isfile(graph_path):
                    graph_dict[model_name] = deserialize(graph_path)
                    logger.info('Graph model [{}] loading completed', sub_model_dir)

            except CustomException as ex:
                logger.warning(ex)
            continue

    graph_index = None
    if index:
        graph_index_path = os.path.join(directory, 'index.bin')
        if os.path.isfile(graph_index_path):
            graph_index = deserialize(graph_index_path)
            logger.info('Graph index file [{}] loaded successfully', graph_index_path)

        return graph_dict, graph_index
    else:
        return graph_dict


def service_cut(
        base_graph: MultiDiGraph,
        network_index: NetworkxIndex,
        start_nodes: list[int] = None,
        node_types: list[ENode] = None,
        edge_types: list[ERelation] = None,
        direction: EExpand = EExpand.Dual,
) -> MultiDiGraph:
    if start_nodes is None:
        start_nodes = []
    if node_types is None:
        node_types = [ENode.Method, ENode.Local, ENode.Member]
    if edge_types is None:
        edge_types = [ERelation.Call, ERelation.Data, ERelation.Control, ERelation.Return, ERelation.Value]

    subgraph = network_slice(base_graph, network_index, start_nodes, node_types, edge_types, direction)

    return subgraph


def service_gen_analysis(
        G: nx.MultiDiGraph,
        weight_dict: dict,
        sum_tag: bool,

):
    return multi_to_single(G, weight_dict, 'r_key', sum_tag)


def service_get_path(
        G: nx.DiGraph,
        start,
        end,
        tag='all',
        max_len=-1
):
    if not isinstance(G, nx.DiGraph):
        raise CustomException(
            ErrorCode.Parameter_Error,
            f'Abnormal graph object'
        )

    if not G.has_node(start):
        raise CustomException(
            ErrorCode.Parameter_Error,
            f'The starting node is not in the graph'
        )

    if not G.has_node(end):
        raise CustomException(
            ErrorCode.Parameter_Error,
            f'The termination node is not in the graph'
        )

    nodes = []
    edges = []

    if tag == 'all':
        paths = networkx_all_paths(G, start, end, max_len)

        for path in map(nx.utils.pairwise, paths):
            tNodes = set()
            tEdges = []
            for u, v in list(path):
                tNodes.add(u)
                tNodes.add(v)
                tEdges.append((u, v))
            edges.append(tEdges)
            nodes.append(list(tNodes))
    elif tag == 'shortest':
        paths = networkx_shortest_path(G, start, end)
        front = None
        for node in paths:
            nodes.append(node)
            if front:
                edges.append((front, node))
            front = node

    return nodes, edges


def service_get_sub_tree(
        G: nx.DiGraph,
        root,
        direction,
        max_dep,
):
    if not isinstance(G, nx.DiGraph):
        raise CustomException(
            ErrorCode.Parameter_Error,
            f'Abnormal graph object'
        )

    if not G.has_node(root):
        raise CustomException(
            ErrorCode.Parameter_Error,
            f'The root node is not in the graph'
        )

    if direction is None or direction == 'succ' or direction == EExpand.Successor:
        succ_dir = True
    else:
        succ_dir = False

    return networkx_tree(G, root, succ_dir, max_dep)


def service_get_subgraph(
        G: nx.DiGraph,
        init_nodes: list,
        node_types: list[ENode] = None,
        direction: EExpand = EExpand.Successor,
        max_depth=-1,
):
    if not isinstance(G, nx.DiGraph):
        raise CustomException(
            ErrorCode.Parameter_Error,
            f'Abnormal graph object'
        )

    if init_nodes:
        return networkx_subgraph(G, init_nodes, node_types, direction, max_depth, 'node_type')

    else:
        raise CustomException(
            ErrorCode.Parameter_Error,
            f'Initial node not specified'
        )


def __service_save_network_index__(
        output_dir: str,
        network_index: NetworkxIndex
):
    if output_dir is None:
        raise CustomException(ErrorCode.Command_Error, f'The save address of the image index file cannot be empty')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if network_index is not None:
        serialize_in_dir(output_dir, 'index', network_index)

    pass


def __service_save_graph__(
        output_dir: str,
        model_name: str | None,
        graph: MultiDiGraph | DiGraph,
) -> None:
    if output_dir is None:
        raise CustomException(ErrorCode.Command_Error, f'The save address of the image file cannot be empty')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if model_name is None:
        save_dir = output_dir
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
    else:
        save_dir = os.path.join(output_dir, model_name)
        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)
        os.makedirs(save_dir)

    serialize_in_dir(save_dir, 'graph', graph)

    network_save_graph_structure(graph, f'{save_dir}')

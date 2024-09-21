import json
import multiprocessing
import os
import sys
from multiprocessing import Queue

from loguru import logger

from ccft.algorithms.alg_multi_to_single import multi_to_single
from ccft.cmd.cmd_json import JsonInstructionConverter
from ccft.cmd.cmd_text import TextInstructionConverter
from ccft.cmd.instruction_converter import InstructionConverter
from ccft.conn.base_conn import AbstConn
from ccft.conn.socket_conn import SocketConn
from ccft.core.constant import ERelation, EExpand
from ccft.service import service_load_graph, service_parse_src, service_parse_cpg, service_cut, \
    __service_save_graph__, service_gen_analysis, service_get_path, service_get_subgraph, service_get_sub_tree
from ccft.util.exceptions.error_code import ErrorCode
from ccft.util.exceptions.exception import CustomException
from ccft.viewer.gen_pciture import get_picture


def main(configs: dict):
    logger.info('application directory {}', configs['application-dir'])

    server: AbstConn
    queue: Queue = multiprocessing.Queue(50)

    if configs['mode'] == 'local':
        graphs, index = service_load_graph(r'D:\Projects\CCFTools\proj0\ParseModel\demo1', dict())
        weight_dict = {
            ERelation.Control: 0.5,
            ERelation.Data: 0.2,
            ERelation.Call: 0.1,
        }
        analysis = multi_to_single(graphs['topic'], weight_dict, 'r_key', False)

        __service_save_graph__(r'D:\Projects\CCFTools\proj0\ParseModel\demo1', 'test-save', analysis)
        get_picture(analysis, title='analysis', label='name', edge_label='weight')

        logger.info('test sub graph')
        subgraph = service_get_subgraph(analysis, [252])
        get_picture(subgraph, title='test subgraph', label='name', edge_label='weight')

        logger.info('test path')
        paths = service_get_path(analysis, 252, 229)
        logger.info('paths: {}', paths)
        pass
    else:
        instruction_converter = JsonInstructionConverter()
        if configs['cmd-fmt'] == 'text':
            instruction_converter = TextInstructionConverter()

        if configs['mode'] == 'net':
            logger.info('net start...')
            server = SocketConn(configs['ip'], configs['port'], queue, instruction_converter)
            if server.start():
                multiprocessing.Process(
                    target=handle_commands,
                    args=(queue, server, configs, instruction_converter)
                ).start()
            else:
                logger.error('启动失败，未建立通信')


def handle_commands(queue: Queue, server: AbstConn, configs: dict, converter: InstructionConverter):
    while True:
        if not queue.empty():
            instruction: str = queue.get()
            logger.info('Receive instructions\n[{}]', instruction)

            action = converter.get_action(instruction)

            if action == 'exit':
                break

            else:
                _handle_command_(instruction, action, server, configs, converter)

    logger.info("exit with code 0")
    pass


def _handle_command_(
        instruction: str,
        action: str,
        server: AbstConn,
        configs: dict,
        converter: InstructionConverter
) -> None:
    cmd_id = converter.get_id(instruction)

    try:
        # parse start
        if action == 'parse-source-code':
            logger.info('Start [parsing source code]')
            src_dir, cpg_path, neo4jcsv_dir, parse_model_dir = converter.parse_sourcecode_instruction(
                instruction)
            service_parse_src(src_dir, cpg_path, neo4jcsv_dir, configs['parse'], configs['export'])
            logger.info('[Source Code Analysis] Completed')
            server.reply(cmd_id=cmd_id, status=True)
        elif action == 'parse-cpg':
            logger.info('Start [parsing CPG file]')
            parse_model_dir, neo4jcsv_dir = converter.parse_cpg_instruction(instruction)
            configs['parse-model-dir'] = parse_model_dir
            logger.info('Update the graph parsing model level address to [{}]', configs['parse-model-dir'])
            configs['parse-model-dict'], configs['parse-model-index'] = service_parse_cpg(parse_model_dir, neo4jcsv_dir)
            logger.info('[Analyze CPG file] Generate')
            server.reply(cmd_id=cmd_id, status=True)
        # parse end

        # load start
        elif action == 'load-model':
            logger.info('Start [Loading Model]')
            model_dir, model_from = converter.load_model_instruction(instruction)
            if model_from == 'parse':
                logger.info('Load parsing level model')
                if configs['parse-model-dir'] is None or model_dir != configs['parse-model-dir']:
                    configs['parse-model-dir'] = model_dir
                    logger.info('Update the graph parsing model level address to [{}]', configs['parse-model-dir'])
                    configs['parse-model-dict'].clear()
                configs['parse-model-dict'], configs['parse-model-index'] = service_load_graph(
                    model_dir,
                    configs['parse-model-dict']
                )
            elif model_from == 'analysis':
                logger.info('Load analysis level model')
                if configs['analysis-model-dir'] is None or model_dir != configs['analysis-model-dir']:
                    configs['analysis-model-dir'] = model_dir
                    logger.info('Update the address of the graph analysis model to [{}]', configs['analysis-model-dir'])
                    configs['analysis-model-dict'].clear()
                configs['analysis-model-dict'] = service_load_graph(
                    model_dir,
                    configs['analysis-model-dict'],
                    index=False
                )
            else:
                raise CustomException(ErrorCode.Parameter_Error, f'Model type [{model_from}] does not exist')
            logger.info('[Loading Model] Completed')
            server.reply(cmd_id=cmd_id, status=True)
        # load end

        # cut start
        elif action == 'cut-parse-model':
            logger.info('Start [parsing level model clipping]')
            base_graph_name, sub_graph_name, start_nodes, node_types, relations, direction \
                = converter.cut_parse_model_instruction(instruction)
            if base_graph_name not in configs['parse-model-dict']:
                raise CustomException(ErrorCode.Parameter_Error, f'The benchmark graph parsing model [{base_graph_name}] does not exist')

            subgraph = service_cut(base_graph=configs['parse-model-dict'][base_graph_name],
                                   network_index=configs['parse-model-index'], start_nodes=start_nodes,
                                   node_types=node_types, edge_types=relations, direction=direction)
            logger.info('Execution of slicing to generate parsing level model completed ')
            __service_save_graph__(configs['parse-model-dir'], sub_graph_name, subgraph)
            configs['parse-model-dict'][sub_graph_name] = subgraph
            logger.info('Slice generation parsing level model has been saved to [{}]', os.path.join(configs['parse-model-dir'], sub_graph_name))
            logger.info('[Analysis level model clipping] completed')
            server.reply(cmd_id=cmd_id, status=True)
        # cut end

        # gen start
        elif action == 'gen-analysis-model':
            logger.info('Start [Generate Graph Analysis Model]')
            sub_parse_model_name, directory, weight_dict, sum_tag = converter.gen_analysis_instruction(instruction)
            if sub_parse_model_name not in configs['parse-model-dict']:
                raise CustomException(
                    ErrorCode.Parameter_Error,
                    f'The benchmark graph parsing model [{sub_parse_model_name}] does not exist',
                )

            analysis_graph = service_gen_analysis(
                configs['parse-model-dict'][sub_parse_model_name],
                weight_dict=weight_dict,
                sum_tag=sum_tag
            )
            logger.info('Graph analysis model generation')

            __service_save_graph__(directory, None, analysis_graph)
            logger.info('The graph analysis model has been saved to [{}]', directory)
            logger.info('[Generate Graph Analysis Model] Completed')
            server.reply(cmd_id=cmd_id, status=True)
        # gen end

        # get start
        elif action == 'get-path':
            logger.info('Start [Search Node Path]')
            tag, model_from, base_graph, start, end, max_len = converter.get_path_instruction(instruction)

            if model_from == 'parse':
                graphs = configs['parse-model-dict']
            elif model_from == 'analysis':
                graphs = configs['analysis-model-dict']
            else:
                raise CustomException(ErrorCode.Parameter_Error, f'Model type [{model_from}] does not exist')

            if base_graph not in graphs:
                raise CustomException(ErrorCode.Parameter_Error, f'The graph {base_graph} is not in the model type [{model_from}]')

            graph = graphs[base_graph]
            nodes, edges = service_get_path(graph, start, end, tag, max_len)
            logger.info('[Search Node Path] Completed')
            server.reply(cmd_id=cmd_id, status=True, nodes=nodes, edges=edges)
        elif action == 'get-tree':
            logger.info('Start [Search Node Expansion Tree]')
            model_from, base_graph, root, direction, max_dep = converter.get_tree_instruction(instruction)

            if model_from == 'parse':
                graphs = configs['parse-model-dict']
            elif model_from == 'analysis':
                graphs = configs['analysis-model-dict']
            else:
                raise CustomException(ErrorCode.Parameter_Error, f'Model type [{model_from}] does not exist')

            if base_graph not in graphs:
                raise CustomException(ErrorCode.Parameter_Error, f'The graph {base_graph} is not in the model type [{model_from}]')

            graph = graphs[base_graph]
            sub_tree = service_get_sub_tree(graph, root, direction, max_dep)
            nodes = [node for node in sub_tree.nodes()]
            if direction == EExpand.Successor:
                edges = [(u, v) for u, v in sub_tree.edges()]
            else:
                edges = [(v, u) for u, v in sub_tree.edges()]

            logger.info('[Search Node Tree] Completed')
            server.reply(cmd_id=cmd_id, status=True, nodes=nodes, edges=edges)
        elif action == 'get-graph':
            logger.info('Start [Search for related nodes]')
            model_from, base_graph, nodes, init_types, direction, max_dep = converter.get_subgraph_instruction(instruction)

            if model_from == 'parse':
                graphs = configs['parse-model-dict']
            elif model_from == 'analysis':
                graphs = configs['analysis-model-dict']
            else:
                raise CustomException(ErrorCode.Parameter_Error, f'Model type [{model_from}] does not exist')

            if base_graph not in graphs:
                raise CustomException(ErrorCode.Parameter_Error, f'The graph {base_graph} is not in the model type [{model_from}]')

            graph = graphs[base_graph]
            subgraph = service_get_subgraph(graph, nodes, init_types, direction, max_dep)
            nodes = [node for node in subgraph.nodes()]
            edges = [(u, v) for u, v in subgraph.edges()]

            logger.info('[Search for related nodes] Completed')
            server.reply(cmd_id=cmd_id, status=True, nodes=nodes, edges=edges)
        # get end

        else:
            raise CustomException(ErrorCode.Command_NotKnow, 'Unknown command, please check if the command is correct')

    except CustomException as ex:
        logger.exception(ex)
        server.reply(cmd_id=cmd_id, status=False, message=ex.__str__())
    except Exception as ex:
        logger.exception(ex)
        server.reply(cmd_id=cmd_id, status=False, message=ex.__str__())


def load_config(application_dir):
    joern_cli_dir = os.path.join(application_dir, 'tools', 'joern-cli')

    configs = {
        'application-dir': application_dir,
        'mode': 'net',
        'ip': '127.0.0.1',
        'port': 8192,
        'cmd-fmt': 'text',
        'debug': False,
        'parse-model-dir': None,
        'analysis-model-dir': None,
        'parse-model-dict': dict(),
        'analysis-model-dict': dict(),
        'parse': os.path.join(joern_cli_dir, 'joern-parse.bat'),
        'export': os.path.join(joern_cli_dir, 'joern-export.bat')
    }

    config_path = os.path.join(application_dir, 'config.json')
    if os.path.isfile(config_path):
        with open(config_path, 'r') as config_file:
            contents = json.loads(config_file.read())
            if 'mode' in contents:
                configs['mode'] = contents['mode']
            if 'debug' in contents:
                configs['debug'] = contents['debug']
            if 'pipe' in contents:
                configs['pipe'] = contents['pipe']
            if 'ip' in contents:
                configs['ip'] = contents['ip']
            if 'port' in contents:
                configs['port'] = contents['port']
            if 'cmd-fmt' in contents:
                configs['cmd-fmt'] = contents['cmd-fmt']
            pass

    return configs


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('error, no set application directory !!!')
        exit(-1)

    S_Configs = load_config(sys.argv[1])
    main(S_Configs)

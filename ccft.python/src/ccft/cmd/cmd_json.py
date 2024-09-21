import json
import os

from loguru import logger

from ccft.cmd.instruction_converter import InstructionConverter
from ccft.core.constant import ENode, ERelation, EExpand
from ccft.util.exceptions.error_code import ErrorCode
from ccft.util.exceptions.exception import CustomException


class JsonInstructionConverter(InstructionConverter):
    @staticmethod
    def get_action(instruction):
        if isinstance(instruction, str):
            instruction = json.loads(instruction)

        if 'type' in instruction:
            return instruction['type']

        return ''

    @staticmethod
    def get_id(instruction):
        if isinstance(instruction, str):
            instruction = json.loads(instruction)

        if 'id' in instruction:
            return instruction['id']

        return -1

    @staticmethod
    def reply(cmd_id, status, message=None, **params):
        if message is None:
            message = ''

        reply = {'type': 'recv', 'id': cmd_id, 'status': status, 'message': message}

        for key, val in params.items():
            reply[key] = val

        return json.dumps(reply)

    @staticmethod
    def exit() -> str:
        return json.dumps({'type': 'exit'})

    @staticmethod
    def parse_sourcecode_instruction(
            instruction
    ):
        if isinstance(instruction, str):
            instruction = json.loads(instruction)

        commands = instruction['arguments']

        if 'src' in commands:
            src_dir = str(commands['src'])
        else:
            raise CustomException(ErrorCode.Command_Error, 'Source code address not specified')

        if 'output' in commands:
            output_dir = str(commands['output'])
        else:
            raise CustomException(ErrorCode.Command_Error, 'Export address not specified')

        if 'cpg' in commands:
            cpg_path = str(commands['cpg'])
        else:
            cpg_path = os.path.join(output_dir, 'cpg.bin')

        if 'neo4j' in commands:
            neo4jcsv_dir = str(commands['neo4j'])
        else:
            neo4jcsv_dir = os.path.join(output_dir, '.neo4jcsv')

        return src_dir, cpg_path, neo4jcsv_dir, output_dir

    @staticmethod
    def parse_cpg_instruction(
            instruction
    ):
        if isinstance(instruction, str):
            instruction = json.loads(instruction)

        commands = instruction['arguments']

        if 'parse-model-dir' in commands:
            parse_model_dir = str(commands['parse-model-dir'])
        else:
            raise CustomException(ErrorCode.Command_Error, 'No graph parsing model address specified')

        if 'neo4j' in commands:
            neo4jcsv_dir = str(commands['neo4j'])
        else:
            raise CustomException(ErrorCode.Command_Error, 'No specified cpg file address')

        return parse_model_dir, neo4jcsv_dir

    @staticmethod
    def load_model_instruction(
            instruction
    ):
        if isinstance(instruction, str):
            instruction = json.loads(instruction)

        commands = instruction['arguments']

        if 'model-dir' in commands:
            model_dir = str(commands['model-dir'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'No specified graph model level address')

        if 'from' in commands:
            model_from = str(commands['from'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'No specified type of graph model to load')

        return model_dir, model_from

    @staticmethod
    def cut_parse_model_instruction(
            instruction
    ):
        if isinstance(instruction, str):
            instruction = json.loads(instruction)

        commands = instruction['arguments']

        node_types = [ENode.Local, ENode.Member, ENode.Member]
        relations = [ERelation.Data, ERelation.Control, ERelation.Call]
        direction = EExpand.Dual

        if 'base' in commands:
            base_graph_name = str(commands['base'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'Reference map object name not specified')

        if 'name' in commands:
            sub_graph_name = str(commands['name'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'The name of the generated new graph parsing model has not been specified')

        if 'start-nodes' in commands:
            start_nodes = commands['start-nodes']
        else:
            start_nodes = []

        if 'node-types' in commands:
            node_types.clear()
            for node_type in commands['node-types']:
                node_types.append(ENode(node_type))

        if 'relations' in commands:
            relations.clear()
            for relation in commands['relations']:
                relations.append(ERelation(relation))

        if 'direction' in commands:
            direction = EExpand(commands['direction'])

        return base_graph_name, sub_graph_name, start_nodes, node_types, relations, direction

    @staticmethod
    def demo_instruction(instruction):
        if isinstance(instruction, str):
            instruction = json.loads(instruction)

        commands = instruction['arguments']

        node_size = 100
        edge_size = 500

        if 'node-size' in commands:
            node_size = commands['node-size']
        if 'edge-size' in commands:
            edge_size = commands['edge-size']
        if 'network-type' in commands:
            network_type = commands['network-type']
        pass

    @staticmethod
    def gen_analysis_instruction(instruction):
        if isinstance(instruction, str):
            instruction = json.loads(instruction)

        commands = instruction['arguments']

        weight_dict = {
            ERelation.Control: 0.5,
            ERelation.Data: 0.2,
            ERelation.Call: 0.1,
            ERelation.Contain: 0
        }

        sum_tag = True

        if 'parse-model-name' in commands:
            parse_model_name = commands['parse-model-name']
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'Name of unspecified graph parsing model')

        if 'directory' in commands:
            directory = commands['directory']
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'Name of unspecified graph parsing model')

        if 'control' in commands:
            weight_dict[ERelation.Control] = commands['control']
        if 'data' in commands:
            weight_dict[ERelation.Data] = commands['data']
        if 'zero' in commands:
            weight_dict[ERelation.Call] = commands['zero']
        if 'contain' in commands:
            weight_dict[ERelation.Contain] = commands['contain']
        if 'repeat' in commands:
            sum_tag = commands['repeat']

        return parse_model_name, directory, weight_dict, sum_tag

    @staticmethod
    def get_path_instruction(instruction):
        if isinstance(instruction, str):
            instruction = json.loads(instruction)

        commands = instruction['arguments']

        if 'from' in commands:
            model_from = str(commands['from'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'Reference map type not specified')

        if 'base-graph' in commands:
            base_graph = str(commands['base-graph'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'No reference map object specified')

        if 'start' in commands:
            start = int(commands['start'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'No starting node specified')

        if 'end' in commands:
            end = int(commands['end'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'No termination node specified')

        if 'max-len' in commands:
            max_len = int(commands['max-len'])
        else:
            max_len = -1

        if 'tag' in commands:
            tag = str(commands['tag'])
        else:
            tag = 'all'
            logger.info('No path retrieval method specified, default search for all connected paths')

        return tag, model_from, base_graph, start, end, max_len

    @staticmethod
    def get_tree_instruction(instruction) -> tuple[str, str, int, int, int]:
        if isinstance(instruction, str):
            instruction = json.loads(instruction)

        commands = instruction['arguments']

        if 'from' in commands:
            model_from = str(commands['from'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'Reference map type not specified')

        if 'base-graph' in commands:
            base_graph = str(commands['base-graph'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'No reference map object specified')

        if 'root' in commands:
            root = int(commands['root'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'No starting node specified')

        if 'direction' in commands:
            direction = None
            direction_val = commands['direction']
            if isinstance(direction_val, str):
                if direction_val.lower().startswith('succ'):
                    direction = EExpand.Successor
                elif direction_val.lower().startswith('pred'):
                    direction = EExpand.Predecessor
            elif isinstance(direction_val, int):
                direction = EExpand(direction_val)
            if direction is None:
                raise CustomException(ErrorCode.Command_NotFound, 'Abnormal parameter settings for expansion direction')
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'No termination node specified')

        if 'max-dep' in commands:
            max_dep = int(commands['max-dep'])
        else:
            max_dep = -1

        return model_from, base_graph, root, direction, max_dep

    @staticmethod
    def get_subgraph_instruction(instruction) -> tuple[str, str, list, list, EExpand, int]:
        if isinstance(instruction, str):
            instruction = json.loads(instruction)

        commands = instruction['arguments']

        if 'from' in commands:
            model_from = str(commands['from'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'Reference map type not specified')

        if 'base-graph' in commands:
            base_graph = str(commands['base-graph'])
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'No reference map object specified')

        if 'nodes' in commands:
            nodes = commands['nodes']
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'Initial node not specified')

        if 'init-types' in commands:
            init_types = commands['init-types']
        else:
            init_types = None

        if 'direction' in commands:
            direction = None
            direction_val = commands['direction']
            if isinstance(direction_val, str):
                if direction_val.lower().startswith('succ'):
                    direction = EExpand.Successor
                elif direction_val.lower().startswith('pred'):
                    direction = EExpand.Predecessor
                elif direction_val.lower().startswith('dual'):
                    direction = EExpand.Dual
            elif isinstance(direction_val, int):
                direction = EExpand(direction_val)
            if direction is None:
                raise CustomException(ErrorCode.Command_NotFound, 'Abnormal parameter settings for expansion direction')
        else:
            raise CustomException(ErrorCode.Command_NotFound, 'No termination node specified')

        if 'max-dep' in commands:
            max_dep = int(commands['max-dep'])
        else:
            max_dep = -1

        return model_from, base_graph, nodes, init_types, direction, max_dep

    @staticmethod
    def get_path_return(cmd_id, status, paths):
        ret = {'type': 'recv', 'id': cmd_id, 'status': status}
        pass

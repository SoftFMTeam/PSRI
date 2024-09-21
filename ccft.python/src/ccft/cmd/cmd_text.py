import os

from ccft.cmd.instruction_converter import InstructionConverter
from ccft.core.constant import ENode, ERelation, EExpand
from ccft.util.exceptions.error_code import ErrorCode
from ccft.util.exceptions.exception import CustomException


class TextInstructionConverter(InstructionConverter):
    @staticmethod
    def get_action(instruction):
        action = instruction.split(' ')[0][2:]
        return action

    @staticmethod
    def get_id(instruction):
        cmds = instruction.split(' ')
        if len(cmds) > 1:
            return instruction.split(' ')[1]
        return -1

    @staticmethod
    def reply(cmd_id, status, message=None, **params):
        if status:
            recv_status = 'ok'
        else:
            recv_status = 'fail'

        if message is None:
            reply = f'--reply {cmd_id} {recv_status}'
        else:
            reply = f'--reply {cmd_id} {recv_status} {message}'

        return reply

    @staticmethod
    def exit() -> str:
        return '--exit'

    @staticmethod
    def parse_sourcecode_instruction(
            instruction
    ):
        commands = [item.strip() for item in instruction.split(' ') if item.strip() != '']
        commands_len = len(commands)

        src_dir = None
        cpg_path = None
        neo4jcsv_dir = None
        output_dir = None

        for index in range(commands_len):
            key = commands[index]
            if key == '-src' or key == '-s' or key == '-S':
                index += 1
                src_dir = str(commands[index])
            elif key == '-output' or key == '-o' or key == '-O':
                index += 1
                output_dir = commands[index]
            elif key == '-cpg' or key == '-c' or key == '-C':
                index += 1
                cpg_path = commands[index]
            elif key == '-neo4j' or key == '-n' or key == '-N':
                index += 1
                neo4jcsv_dir = commands[index]

        if src_dir is None:
            raise CustomException(ErrorCode.Command_Error, 'The parsing instruction is missing [- src]', 'Parsing instruction processing')
        if output_dir is None:
            raise CustomException(ErrorCode.Command_Error, 'The parsing instruction is missing [- output]', 'Parsing instruction processing')
        if not os.path.isdir(src_dir):
            raise CustomException(ErrorCode.Dir_NotFound, f'The source code address [{src_dir}] does not exist', 'Parsing instruction processing')

        if cpg_path is None:
            cpg_path = os.path.join(output_dir, 'cpg.bin')

        if neo4jcsv_dir is None:
            neo4jcsv_dir = os.path.join(output_dir, '.neo4jcsv')

        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        return src_dir, cpg_path, neo4jcsv_dir, output_dir

    @staticmethod
    def parse_cpg_instruction(
            instruction
    ):
        commands = [item.strip() for item in instruction.split(' ') if item.strip() != '']
        commands_len = len(commands)

        neo4jcsv_dir = None
        output_dir = None

        for index in range(commands_len):
            key = commands[index]
            if key == '-output' or key == '-o' or key == '-O':
                index += 1
                output_dir = str(commands[index])
            elif key == '-neo4j' or key == '-n' or key == '-N':
                index += 1
                neo4jcsv_dir = str(commands[index])

        if output_dir is None:
            raise CustomException(ErrorCode.Command_Error, 'Analysis instruction is missing [- output]', 'Analyze instruction processing')

        if neo4jcsv_dir is None:
            neo4jcsv_dir = os.path.join(output_dir, '.neo4jcsv')

        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        return output_dir, neo4jcsv_dir

    @staticmethod
    def load_model_instruction(
            instruction
    ):
        commands = [item.strip() for item in instruction.split(' ') if item.strip() != '']
        commands_len = len(commands)

        graph_space = ''

        for index in range(commands_len):
            key = commands[index]
            if key == '-dir' or key == '-d' or key == '-D':
                index += 1
                graph_space = commands[index]

        if not graph_space.strip():
            raise CustomException(ErrorCode.Command_NotFound, 'The read instruction is missing [- dir]', 'Loading instruction processing')

        if not os.path.isdir(graph_space):
            raise CustomException(ErrorCode.Dir_NotFound, f'Image project address\'{graph_space}\'absent')

        return graph_space

    @staticmethod
    def cut_parse_model_instruction(
            instruction
    ):
        commands = [item.strip() for item in instruction.split(' ') if item.strip() != '']
        commands_len = len(commands)

        base_graph_name = 'basic'
        sub_graph_name = 'sub_graph'
        start_nodes = []
        node_types = [ENode.Local, ENode.Member, ENode.Member]
        edge_types = [ERelation.Data, ERelation.Control, ERelation.Call]
        direction = EExpand.Dual

        for index in range(commands_len):
            key = commands[index]
            if key == '-base' or key == '-b' or key == '-B':
                index += 1
                base_graph_name = commands[index]
            elif key == '-name' or key == '-n' or key == '-N':
                index += 1
                sub_graph_name = commands[index]
            elif key == '-start-nodes' or key == '-s' or key == '-S':
                index += 1
                node_cmd: str = commands[index]
                nodes = [item.strip() for item in node_cmd.split(',') if item.strip().isdigit()]
                for node in nodes:
                    start_nodes.append(int(node))
            elif key == '-node-types' or key == '-t' or key == '-T':
                index += 1
                type_cmd = commands[index]
                node_types.clear()
                types = [item.strip().lower() for item in type_cmd.split(',') if item.strip()]
                for node_type in types:
                    if node_type == 'local':
                        node_types.append(ENode.Local)
                    elif node_type == 'member':
                        node_types.append(ENode.Member)
                    elif node_type == 'method':
                        node_types.append(ENode.Method)
                    elif node_type == 'type_decl':
                        node_types.append(ENode.TypeDecl)
                    elif node_type == 'file':
                        node_types.append(ENode.File)
            elif key == '-relations' or key == '-r' or key == '-R':
                index += 1
                edge_cmd: str = commands[index]
                edge_types.clear()
                types = [item.strip().lower() for item in edge_cmd.split(',') if item.strip()]
                for edge_type in types:
                    if edge_type == 'call':
                        edge_types.append(ERelation.Call)
                    elif edge_type == 'data':
                        edge_types.append(ERelation.Data)
                    elif edge_type == 'control':
                        edge_types.append(ERelation.Control)
                    elif edge_type == 'contain':
                        edge_types.append(ERelation.Contain)
            elif key == '-direction' or key == '-d' or key == '-D':
                index += 1
                if commands[index] == 'pre':
                    direction = EExpand.Predecessor
                elif commands[index] == 'post':
                    direction = EExpand.Successor

        return base_graph_name, sub_graph_name, start_nodes, node_types, edge_types, direction

import csv
import os

import pandas as pd


def read_edge_data(edge_data_path: str):
    successors: dict[int, set] = dict()
    predecessors: dict[int, set] = dict()

    if os.path.isfile(edge_data_path):
        with open(edge_data_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                start_id = int(row[0])
                end_id = int(row[1])

                if start_id not in successors:
                    successors[start_id] = set()
                successors[start_id].add(end_id)

                if end_id not in predecessors:
                    predecessors[end_id] = set()
                predecessors[end_id].add(start_id)

    return successors, predecessors


def read_node_data(node_data_path: str, header_path: str) -> dict[int, dict]:
    if os.path.isfile(header_path) and os.path.isfile(node_data_path):
        data_header = read_header_file(header_path)
        data = pd.read_csv(node_data_path, header=None, encoding='utf-8')
        data.columns = data_header
        data.set_index(['ID'], drop=True, inplace=True)
        data.dtypes['ID'] = int
        data.dtypes['NAME'] = str
        data.dtypes['SIGNATURE'] = str

        return data.to_dict(orient='index')
    else:
        return dict()


def read_header_file(header_path):
    datas = pd.read_csv(header_path)
    headers = []
    for head in datas.columns:
        head_values = head.split(':')
        for value in head_values:
            if value:
                headers.append(value)
                break

    return headers


class Neo4jCsvReader:
    def __init__(self, neo4jcsv_dir: str):
        self.data_directory = neo4jcsv_dir

        self.node_binging = self.__read_node_data('BINDING')
        self.node_blocks = self.__read_node_data('BLOCK')
        self.node_calls = self.__read_node_data('CALL')
        self.node_control_structures = self.__read_node_data('CONTROL_STRUCTURE')
        self.node_dependencies = self.__read_node_data('DEPENDENCY')
        self.node_field_identifiers = self.__read_node_data('FIELD_IDENTIFIER')
        self.node_files = self.__read_node_data('FILE')
        self.node_identifiers = self.__read_node_data('IDENTIFIER')
        self.node_imports = self.__read_node_data('IMPORT')
        self.node_jump_targets = self.__read_node_data('JUMP_TARGET')
        self.node_literals = self.__read_node_data('LITERAL')
        self.node_locals = self.__read_node_data('LOCAL')
        self.node_members = self.__read_node_data('MEMBER')
        self.node_methods = self.__read_node_data('METHOD')
        self.node_method_parameter_ins = self.__read_node_data('METHOD_PARAMETER_IN')
        self.node_method_parameter_outs = self.__read_node_data('METHOD_PARAMETER_OUT')
        self.node_method_refs = self.__read_node_data('METHOD_REF')
        self.node_method_returns = self.__read_node_data('METHOD_RETURN')
        self.node_modifiers = self.__read_node_data('MODIFIER')
        self.node_namespace_blocks = self.__read_node_data('NAMESPACE_BLOCK')
        self.node_namespaces = self.__read_node_data('NAMESPACE')
        self.node_returns = self.__read_node_data('RETURN')
        self.node_types = self.__read_node_data('TYPE')
        self.node_type_decls = self.__read_node_data('TYPE_DECL')
        self.node_unknowns = self.__read_node_data('UNKNOWN')

        self.type_nodes_dict = {
            'binging': self.node_binging,
            'block': self.node_blocks,
            'call': self.node_calls,
            'control_structure': self.node_control_structures,
            'dependency': self.node_dependencies,
            'field_identifier': self.node_field_identifiers,
            'file': self.node_files,
            'identifier': self.node_identifiers,
            'import': self.node_imports,
            'jump_target': self.node_jump_targets,
            'literal': self.node_literals,
            'local': self.node_locals,
            'member': self.node_members,
            'method': self.node_methods,
            'method_parameter_in': self.node_method_parameter_ins,
            'method_parameter_out': self.node_method_parameter_outs,
            'method_ref': self.node_method_refs,
            'method_return': self.node_method_returns,
            'modifier': self.node_modifiers,
            'namespace_block': self.node_namespace_blocks,
            'namespace': self.node_namespaces,
            'return': self.node_returns,
            'type': self.node_types,
            'type_decl': self.node_type_decls,
            'unknown': self.node_unknowns,
        }

        self.edge_alias_of = self.__read_edge_data('ALIAS_OF')
        self.edge_argument = self.__read_edge_data('ARGUMENT')
        self.edge_ast = self.__read_edge_data('AST')
        self.edge_binds = self.__read_edge_data('BINDS')
        self.edge_call = self.__read_edge_data('CALL')
        self.edge_cdg = self.__read_edge_data('CDG')
        self.edge_cfg = self.__read_edge_data('CFG')
        self.edge_condition = self.__read_edge_data('CONDITION')
        self.edge_contain = self.__read_edge_data('CONTAINS')
        self.edge_dominate = self.__read_edge_data('DOMINATE')
        self.edge_eval_type = self.__read_edge_data('EVAL_TYPE')
        self.edge_imports = self.__read_edge_data('IMPORTS')
        self.edge_inherits_from = self.__read_edge_data('INHERITS_FROM')
        self.edge_parameter_link = self.__read_edge_data('PARAMETER_LINK')
        self.edge_post_dominate_link = self.__read_edge_data('POST_DOMINATE')
        self.edge_reaching_def = self.__read_edge_data('REACHING_DEF')
        self.edge_receiver = self.__read_edge_data('RECEIVER')
        self.edge_ref = self.__read_edge_data('REF')
        self.edge_source_file = self.__read_edge_data('SOURCE_FILE')

    def is_node_in(self, node_id, node_type):
        if node_type in self.type_nodes_dict:
            return node_id in self.type_nodes_dict[node_type]
        return False

    def find_node(self, node_id) -> tuple[dict, str]:
        if node_id is not None:
            for node_type in self.type_nodes_dict:
                nodes = self.type_nodes_dict[node_type]
                if node_id in nodes:
                    return nodes[node_id], node_type
        return dict(), ''

    def find_node_in(self, node_id, node_type) -> tuple[dict, str]:
        if node_id is not None and node_type in self.type_nodes_dict:
            nodes = self.type_nodes_dict[node_type]
            if node_id in nodes:
                return nodes[node_id], node_type
        return dict(), ''

    def __read_edge_data(self, data_name: str):
        data_path = '%s\\edges_%s_data.csv' % (self.data_directory, data_name)
        return read_edge_data(data_path)

    def __read_node_data(self, data_name):
        node_data_path = '%s\\nodes_%s_data.csv' % (self.data_directory, data_name)
        header_path = '%s\\nodes_%s_header.csv' % (self.data_directory, data_name)
        return read_node_data(node_data_path, header_path)

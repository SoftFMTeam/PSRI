import networkx
import pandas as pd
from loguru import logger

from ccft.core.constant import ENode, ERelation
from ccft.helper.neo4jcsv.neo4jcsv_functions import _find_successors, _get_successor_tree
from ccft.helper.neo4jcsv.neo4jcsv_reader import Neo4jCsvReader
from ccft.helper.network_index import NetworkxIndex

operator_fullname = set()


class Neo4JCsvLinkMethods:
    def __init__(self, reader: Neo4jCsvReader, index: NetworkxIndex, multi_graph: networkx.MultiDiGraph):
        self.reader = reader
        self.multi_graph = multi_graph
        self.index = index

        self.handle()
        pass

    def handle(self):
        logger.debug('Start linking function information')
        method_ids = self.index.get_nodes(etp=ENode.Method)
        methods_count = len(method_ids)
        for idx in range(methods_count):
            method_id = method_ids[idx]
            operators = []
            operands = []
            self.__link_method(method_id, self.multi_graph.nodes[method_id], operators, operands)
            method_attrs = self.multi_graph.nodes[method_id]
            successors = self.multi_graph.successors(method_id)
            for successor in successors:
                for key, data in self.multi_graph.get_edge_data(method_id, successor).items():
                    if data['r_key'] == ERelation.Data.value:
                        method_attrs['con_df'] += 1
                    elif data['r_key'] == ERelation.Call.value:
                        method_attrs['con_zc'] += 1
                    elif data['r_key'] == ERelation.Control.value:
                        method_attrs['con_cf'] += 1
                    elif data['r_key'] == ERelation.Value.value:
                        method_attrs['con_val'] += 1
                    elif data['r_key'] == ERelation.Return.value:
                        method_attrs['con_rf'] += 1
            method_attrs['number_of_operators'] = len(operators)
            method_attrs['set_of_operators'] = len(set(operators))
            method_attrs['number_of_operands'] = len(operands)
            method_attrs['set_of_operands'] = len(set(operands))
            pass

        logger.debug('Function information link completed')

        # logger.info('All operators：{}', operator_fullname)

    def _add_edge(
            self,
            source,
            source_attr,
            target,
            target_attr,
            relation_key: ERelation,
            line_number: int = -1,
    ):
        edges = []

        if source == target:
            return

        source_ntp = ENode(source_attr['node_type'])
        target_ntp = ENode(target_attr['node_type'])

        if source_ntp == ENode.Method:
            if target_ntp == ENode.Method and (relation_key == ERelation.Data or relation_key == ERelation.Call):
                source_attr['fan_out'] += 1
                target_attr['fan_in'] += 1

        if target_ntp == ENode.Method:
            if relation_key == ERelation.Control:
                edges.append((ERelation.Control, 'control_method'))
            elif relation_key == ERelation.Data:
                edges.append((ERelation.Data, 'data_method'))
            elif relation_key == ERelation.Call:
                edges.append((ERelation.Call, 'call_method'))
            elif relation_key == ERelation.Return:
                edges.append((ERelation.Return, 'return_method'))
            else:
                logger.error('Wrong [Method] connection {}({}) -> {}({}) [{}]',
                             source_ntp.name, source, target_ntp.name, target, relation_key.name)

        elif target_ntp == ENode.Local or target_ntp == ENode.Member:
            edges.append((ERelation.Value, 'value_local'))
            source_attr['fan_out'] += 1
            target_attr['fan_in'] += 1

            if relation_key == ERelation.Control:
                edges.append((ERelation.Control, 'control_local'))

        for r_key, r_label in edges:
            # todo debug
            # source_name = self.multi_graph.nodes[source]['name']
            # target_name = self.multi_graph.nodes[target]['name']
            # logger.info(f'添加边 {source_name}({source}) -> {target_name} ({target}) {target_ntp.name} - {r_label}')

            multi_key = self.multi_graph.add_edge(source, target, source=source, target=target,
                                                  r_key=r_key.value, r_label=r_label, line_number=line_number)
            self.index.set_edge(source, target, r_key, r_label, multi_key)
        pass

    def __link_method(self, method_id: int, method_attrs: dict, operators, operands):
        visited = set()
        # todo debug
        # code = method_attrs['code']
        # logger.debug(f'================================ {method_id} ===================================\n{code}')

        ast_successors = _find_successors(method_id, self.reader.edge_ast, False)
        for succ_id in ast_successors:
            succ_attrs, succ_tp = self.reader.find_node(succ_id)
            self.__handle_statement(method_id, method_attrs, succ_id, succ_attrs, succ_tp,
                                    visited, 1, ERelation.Call, operators, operands)
        pass

    def __handle_statement(
            self,
            method_id: int,
            method_attrs: dict,
            node_id: int,
            node_attrs: dict,
            node_tp: str,
            visited: set,
            cyc: int,
            relation: ERelation,
            operators: list,
            operands: list
    ):
        if node_id in visited:
            return

        # todo debug
        # code = node_attrs['CODE']
        # logger.warning(f'[{node_tp}] - {relation.name} - {node_id} - "{code}"')

        # operator_fullname.add(node_tp)

        if node_tp == 'block':
            visited.add(node_id)
            successors = _find_successors(node_id, self.reader.edge_ast)
            for succ_id in successors:
                succ_attrs, succ_tp = self.reader.find_node(succ_id)
                self.__handle_statement(method_id, method_attrs, succ_id, succ_attrs, succ_tp,
                                        visited, cyc, relation, operators, operands)
        elif node_tp == 'control_structure':
            visited.add(node_id)
            successors = _find_successors(node_id, self.reader.edge_ast)
            method_attrs['mc_cabe'] += 1
            if successors:
                method_attrs['acc_cyc'] += cyc
                condition = True
                for succ_id in successors:
                    succ_attrs, succ_tp = self.reader.find_node(succ_id)
                    if succ_tp == 'block':
                        self.__handle_statement(method_id, method_attrs, succ_id, succ_attrs, succ_tp,
                                                visited, cyc + 1, relation, operators, operands)
                    elif condition:
                        condition = False
                        self.__handle_item(method_id, method_attrs, succ_id, succ_attrs, succ_tp,
                                           visited, cyc, ERelation.Control, False, True, operators, operands)
                        pass
        elif node_tp == 'local':
            pass
        elif node_tp == 'method_parameter_in':
            pass
        elif node_tp == 'method_parameter_out':
            pass
        elif node_tp == 'method_return':
            pass
        else:
            self.__handle_item(method_id, method_attrs, node_id, node_attrs, node_tp,
                               visited, cyc, ERelation.Call, False, False, operators, operands)
        pass

    def __handle_item(
            self,
            method_id: int,
            method_attrs: dict,
            node_id: int,
            node_attrs: dict,
            node_tp: str,
            visited: set,
            cyc: int,
            relation: ERelation,
            assign: bool,
            get_ret: bool,
            operators: list,
            operands: list
    ):
        if node_id in visited:
            return

        # # todo debug
        # code = node_attrs['CODE']
        # logger.warning(f'[{node_tp}] - {relation.name} - {assign} - {node_id} - "{code}"')

        if node_tp == 'call':
            self.__handle_call(method_id, method_attrs, node_id, node_attrs, visited, cyc, relation, assign, get_ret, operators, operands)
        elif node_tp == 'identifier':
            self.__handle_identifier(method_id, method_attrs, node_id, node_attrs, node_tp, visited, relation, operands)

        visited.add(node_id)
        successors = _find_successors(node_id, self.reader.edge_ast)
        for succ_id in successors:
            succ_attrs, succ_tp = self.reader.find_node(succ_id)
            self.__handle_item(method_id, method_attrs, succ_id, succ_attrs, succ_tp,
                               visited, cyc, relation, assign, get_ret, operators, operands)
        pass

    def __handle_call(
            self,
            method_id: int,
            method_attrs: dict,
            node_id: int,
            node_attrs: dict,
            visited: set,
            cyc: int,
            relation: ERelation,
            assign: bool,
            get_ret: bool,
            operators: list,
            operands: list
    ):
        if node_id in visited:
            return

        full_name = node_attrs['METHOD_FULL_NAME']
        if not pd.isna(full_name):
            if full_name.startswith('<operator>'):
                operators.append(full_name)
                if full_name == '<operator>.fieldAccess' or full_name == '<operator>.indirectFieldAccess':
                    var_id, var_ntp = self.__reaching_var_definition(method_id, node_id, node_attrs, 'call', visited)
                    if var_id:
                        self._add_edge(method_id, method_attrs, var_id, self.multi_graph.nodes[var_id],
                                       relation, node_attrs['LINE_NUMBER'])
                elif full_name == '<operator>.assignment':
                    visited.add(node_id)
                    args = _find_successors(node_id, self.reader.edge_argument)
                    first_arg = True

                    for arg_id in args:
                        arg_attrs, arg_tp = self.reader.find_node(arg_id)
                        if first_arg:
                            first_arg = False
                            t_assign = True
                        else:
                            t_assign = assign

                        if relation > ERelation.Data.value:
                            self.__handle_item(method_id, method_attrs, arg_id, arg_attrs, arg_tp, visited,
                                               cyc, relation, t_assign, not t_assign, operators, operands)
                        else:
                            self.__handle_item(method_id, method_attrs, arg_id, arg_attrs, arg_tp, visited,
                                               cyc, ERelation.Data, t_assign, not t_assign, operators, operands)
            call_nodes = _find_successors(node_id, self.reader.edge_call)
            for call_node in call_nodes:
                if self.multi_graph.has_node(call_node):
                    param = self.multi_graph.nodes[call_node]['param']
                    ret_type = self.multi_graph.nodes[call_node]['ret_type']
                    if param:
                        self._add_edge(method_id, method_attrs, call_node, self.multi_graph.nodes[call_node],
                                       ERelation.Data, node_attrs['LINE_NUMBER'])
                    else:
                        self._add_edge(method_id, method_attrs, call_node, self.multi_graph.nodes[call_node],
                                       ERelation.Call, node_attrs['LINE_NUMBER'])
                    if get_ret and ret_type and ret_type != 'void':
                        self._add_edge(method_id, method_attrs, call_node, self.multi_graph.nodes[call_node],
                                       ERelation.Return, node_attrs['LINE_NUMBER'])

                    if relation == ERelation.Control:
                        self._add_edge(method_id, method_attrs, call_node, self.multi_graph.nodes[call_node],
                                       ERelation.Control, node_attrs['LINE_NUMBER'])

                    visited.add(node_id)
                    args = _find_successors(node_id, self.reader.edge_argument)
                    for arg_id in args:
                        succ_attrs, succ_tp = self.reader.find_node(arg_id)
                        self.__handle_item(method_id, method_attrs, arg_id, succ_attrs, succ_tp,
                                           visited, cyc, relation, assign, True, operators, operands)
        visited.add(node_id)
        pass

    def __handle_identifier(
            self,
            method_id: int,
            method_attrs: dict,
            node_id: int,
            node_attrs: dict,
            node_tp: str,
            visited: set,
            relation: ERelation,
            operands: list
    ):
        if node_id in visited:
            return

        operands.append(node_attrs['NAME'])
        var_id, var_ntp = self.__reaching_var_definition(method_id, node_id, node_attrs, node_tp, visited)
        if var_id:
            self._add_edge(method_id, method_attrs, var_id, self.multi_graph.nodes[var_id], relation, node_attrs['LINE_NUMBER'])
        visited.add(node_id)
        return

    def __reaching_var_definition(
            self,
            method_id,
            node_id: int,
            node_attrs: dict,
            node_tp: str,
            visited: set,
    ) -> tuple[int, ENode] | tuple[None, None]:
        if node_id in visited:
            return None, None

        if node_tp == 'call':
            operator_name = node_attrs['METHOD_FULL_NAME']
            if operator_name.startswith('<operator>'):
                operator_name = operator_name[len('<operator>.'):]
            if operator_name == 'fieldAccess' or operator_name == 'indirectFieldAccess':
                args = _find_successors(node_id, self.reader.edge_argument)
                if len(args) == 2:
                    fir_attrs, fir_tp = self.reader.find_node(args[0])
                    type_decls = self.__reaching_datatype(method_id, fir_attrs, fir_tp)
                    sec_attributes, sec_tp = self.reader.find_node(args[1])
                    if sec_tp == 'field_identifier':
                        if type_decls:
                            item_id = self.index.find_item_in_type_decl(sec_attributes['CODE'], type_decls)
                            if item_id is not None:
                                if self.index.is_node_in(item_id, ENode.Member):
                                    return item_id, ENode.Member
        elif node_tp == 'identifier':
            ref_trace = _get_successor_tree(node_id, self.reader.edge_ref)
            if ref_trace:
                def_node_id = ref_trace[0][1][0]
                etp = self.index.get_node_type(def_node_id)
                if etp and etp != ENode.TypeDecl:
                    return def_node_id, etp
            else:
                type_decl_id = self.index.find_type_decl_by_item(method_id)
                if type_decl_id is not None:
                    item_id = self.index.find_item_in_type_decl(node_attrs['NAME'], type_decl_id)
                    etp = self.index.get_node_type(item_id)
                    if etp and etp != ENode.TypeDecl and etp != ENode.Method:
                        return item_id, etp

        return None, None

    def __reaching_datatype(self, method_id: int, node_attrs: dict, node_tp: str) -> list[int]:
        type_decls = []

        if node_tp == 'identifier':
            if node_attrs['TYPE_FULL_NAME'] == 'ANY':
                nodes = self.index.find_nodes(fullname=node_attrs['NAME'], etp=ENode.TypeDecl)
                type_decls.extend(nodes)
            else:
                nodes = self.index.find_nodes(fullname=node_attrs['TYPE_FULL_NAME'], etp=ENode.TypeDecl)
                type_decls.extend(nodes)
        elif node_tp == 'literal' and node_attrs['CODE'] == 'this':
            type_decl_id = self.index.find_type_decl_by_item(method_id)
            type_decls.append(type_decl_id)

        return type_decls

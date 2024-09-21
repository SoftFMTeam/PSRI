import networkx
from loguru import logger

from ccft.core.constant import ENode, ERelation
from ccft.helper.neo4jcsv.neo4jcsv_functions import _is_file, _is_type_decl, _is_method, _is_member, _is_local, \
    _find_successors, _find_precursors
from ccft.helper.neo4jcsv.neo4jcsv_reader import Neo4jCsvReader
from ccft.helper.network_index import NetworkxIndex


class Neo4JCsvExtraNodes:
    def __init__(self, reader: Neo4jCsvReader, index: NetworkxIndex, multi_graph: networkx.MultiDiGraph):
        self.reader = reader
        self.index = index
        self.multi_graph = multi_graph

        self.handle()
        pass

    def handle(self):
        logger.info('Start extracting node information...')

        for file_id, file_attrs in self.reader.node_files.items():
            self.__add_file_node(file_id, file_attrs)
        logger.info('File information extraction completed')

        for index in self.reader.node_members:
            attributes = self.reader.node_members[index]
            self.__add_member_node(index, attributes)
        logger.info('Attribute information extraction completed')

        for method_id, method_attrs in self.reader.node_methods.items():
            self.__add_method_node(method_id, method_attrs)
        logger.info('Function information extraction completed')

        for type_decl_id, type_decl_attrs in self.reader.node_type_decls.items():
            self.__add_type_decl_node(type_decl_id, type_decl_attrs)
        logger.info('Custom structure information extraction completed')

        type_decl_ids = self.index.get_nodes(etp=ENode.TypeDecl)
        for type_decl_id in type_decl_ids:
            self.__link_type_decl(type_decl_id, self.multi_graph.nodes[type_decl_id])
        logger.info('Custom structure link completed')

        file_ids = self.index.get_nodes(etp=ENode.File)
        for file_id in file_ids:
            self.__add_local_in_file(file_id)
        logger.info('Global variable information extraction completed')

        logger.info('Node information extraction completed')
        pass

    def __add_node(self, node_id, name, node_type: ENode,
                   fullname='', signature='', filename='', code='',
                   line_number=-1, line_number_end=-1, column_number=-1, column_number_end=-1,
                   line_of_code=0,
                   number_of_operators=0,
                   set_of_operators=0,
                   number_of_operands=0,
                   set_of_operands=0,
                   fan_in=0,
                   fan_out=0,
                   mc_cabe=1,
                   acc_cyc=1,
                   con_cf=0,
                   con_df=0,
                   con_zc=0,
                   con_rf=0,
                   con_val=0,
                   param=0,
                   param_in=0,
                   param_out=0,
                   ret_type='',
                   ):
        if not self.multi_graph.has_node(node_id):
            self.multi_graph.add_node(
                node_id, id=node_id, name=name, node_type=node_type.value,
                fullname=fullname, signature=signature, filename=filename, code=code,
                line_number=line_number, line_number_end=line_number_end,
                column_number=column_number, column_number_end=column_number_end,
                line_of_code=line_of_code,
                number_of_operators=number_of_operators, set_of_operators=set_of_operators,
                number_of_operands=number_of_operands, set_of_operands=set_of_operands,
                fan_in=fan_in, fan_out=fan_out,
                mc_cabe=mc_cabe, acc_cyc=acc_cyc,
                con_cf=con_cf, con_df=con_df, con_zc=con_zc, con_rf=con_rf, con_val=con_val,
                param=param, param_in=param_in, param_out=param_out, ret_type=ret_type)

            self.index.set_node(node_id, node_type, self.multi_graph.nodes[node_id])
            # todo debug
            # logger.debug(f'Add Node [{node_type.name}] {node_id} {fullname}')
        pass

    def __add_edge(self, source: int, target: int, target_ntp: ENode):
        label = None

        if target_ntp == ENode.Method:
            label = 'contain_method'
        elif target_ntp == ENode.Local:
            label = 'contain_local'
        elif target_ntp == ENode.Member:
            label = 'contain_member'
        elif target_ntp == ENode.TypeDecl:
            label = 'contain_type_decl'

        if label:
            # # todo debug
            # source_name = multi_graph.nodes[source]['name']
            # target_name = multi_graph.nodes[target]['name']
            # logger.info(f'Add Edge {source_name}({source}) -> {target_name} ({target}, {target_ntp}) {label}')

            multi_key = self.multi_graph.add_edge(source, target, source=source, target=target,
                                                  r_key=ERelation.Contain.value, r_label=label, line_number=-1)
            self.index.set_edge(source, target, ERelation.Contain, label, multi_key)
        pass

    def __add_file_node(self, node_id, attributes: dict):
        if not self.multi_graph.has_node(node_id) and _is_file(attributes):
            name = attributes['NAME']
            self.__add_node(node_id=node_id, name=name, node_type=ENode.File)
            self.index.set_node(node_id, ENode.File, self.multi_graph.nodes[node_id])
        pass

    def __add_type_decl_node(self, node_id: int, attributes: dict):
        if not self.multi_graph.has_node(node_id) and _is_type_decl(attributes):
            name = attributes['NAME']
            filename = attributes['FILENAME']
            fullname = attributes['FULL_NAME']
            code = attributes['CODE']

            flag = True

            alias_type = attributes['ALIAS_TYPE_FULL_NAME']
            if isinstance(alias_type, str):
                # eg: typedef uint64_t UINT64;
                # if alias_type == 'ANY':
                #     pass
                # else:
                #     type_id, type_name = self.index.get_alias_by_fullname(alias_type)
                #     if type_id is None:
                #         self.index.set_alias_type_name(node_id, fullname, alias_type)
                #     else:
                #         flag = False
                #         self.index.set_alias_type_name(type_id, fullname, alias_type)
                pass
            if flag:
                self.__add_node(node_id=node_id, name=name, node_type=ENode.TypeDecl,
                                fullname=fullname, filename=filename, code=code)

        pass

    def __add_method_node(self, node_id, attributes: dict):
        if not self.multi_graph.has_node(node_id) and _is_method(attributes):
            name = attributes['NAME']
            filename = attributes['FILENAME']
            fullname = attributes['FULL_NAME']
            signature = attributes['SIGNATURE']
            code = attributes['CODE']
            line_number = attributes['LINE_NUMBER']
            line_number_end = attributes['LINE_NUMBER_END']
            column_number = attributes['COLUMN_NUMBER']
            column_number_end = attributes['COLUMN_NUMBER_END']
            line_of_code = line_number_end - line_number + 1

            ast_nodes = _find_successors(node_id, self.reader.edge_ast)
            param_in = 0
            param_out = 0
            ret_type = 'void'
            for ast_node in ast_nodes:
                if self.reader.is_node_in(ast_node, 'method_parameter_in'):
                    param_in += 1
                elif self.reader.is_node_in(ast_node, 'method_parameter_out'):
                    param_out += 1
                elif self.reader.is_node_in(ast_node, 'method_return'):
                    ret_attrs, ret = self.reader.find_node_in(ast_node, 'method_return')
                    if ret:
                        ret_type = ret_attrs['TYPE_FULL_NAME']

            param = param_in + param_out

            method_id = self.index.find_first_or_default_node(fullname=fullname, etp=ENode.Method)
            if method_id:
                if code.find('{') > 0:
                    self.multi_graph.nodes[method_id]['filename'] = filename
                    self.multi_graph.nodes[method_id]['code'] = code
                    self.multi_graph.nodes[method_id]['line_number'] = line_number
                    self.multi_graph.nodes[method_id]['line_number_end'] = line_number_end
                    self.multi_graph.nodes[method_id]['column_number'] = column_number
                    self.multi_graph.nodes[method_id]['column_number_end'] = column_number_end
                    self.multi_graph.nodes[method_id]['line_of_code'] = line_of_code
                    self.multi_graph.nodes[method_id]['param'] = param
                    self.multi_graph.nodes[method_id]['param_in'] = param_in
                    self.multi_graph.nodes[method_id]['param_out'] = param_out
                    self.multi_graph.nodes[method_id]['ret_type'] = ret_type
            else:
                self.__add_node(node_id=node_id, name=name, node_type=ENode.Method,
                                fullname=fullname, signature=signature, filename=filename, code=code,
                                line_number=line_number, line_number_end=line_number_end,
                                param=param, param_in=param_in, param_out=param_out, ret_type=ret_type,
                                column_number=column_number, column_number_end=column_number_end,
                                line_of_code=line_of_code)
        pass

    def __add_member_node(self, node_id, attributes: dict):
        if not self.multi_graph.has_node(node_id) and _is_member(attributes):
            name = attributes['NAME']
            code = attributes['CODE']

            self.__add_node(node_id=node_id, name=name, node_type=ENode.Member, code=code)
        pass

    def __add_local_node(self, node_id, attributes: dict, filename: str):
        if not self.multi_graph.has_node(node_id) and _is_local(attributes):
            name = attributes['NAME']
            fullname = '%s.%s' % (filename, name)
            code = attributes['CODE']

            self.__add_node(node_id=node_id, name=name, node_type=ENode.Local, fullname=fullname,
                            code=code, filename=filename)
        pass

    def __link_type_decl(self, type_decl_id: int, type_decl_data: dict):
        successors = _find_successors(type_decl_id, self.reader.edge_ast)
        for successor_id in successors:
            if self.reader.is_node_in(successor_id, 'method'):
                method_attrs = self.reader.type_nodes_dict['method'][successor_id]
                fullname = method_attrs['FULL_NAME']
                method_id = self.index.find_first_or_default_node(fullname=fullname, etp=ENode.Method)
                if method_id:
                    self.__add_edge(type_decl_id, method_id, ENode.Method)
                pass
            elif self.reader.is_node_in(successor_id, 'member') and self.index.is_node_in(successor_id, ENode.Member):
                member_attrs = self.multi_graph.nodes[successor_id]
                member_name = member_attrs['name']
                member_attrs['fullname'] = '%s.%s' % (type_decl_data['fullname'], member_name)
                member_attrs['filename'] = type_decl_data['filename']
                self.index.set_node(successor_id, ENode.Member, member_attrs)
                self.__add_edge(type_decl_id, successor_id, ENode.Member)
                pass
            elif self.reader.is_node_in(successor_id, 'type_decl') and self.index.is_node_in(successor_id,
                                                                                             ENode.TypeDecl):
                self.index.add_sub_struct(type_decl_id, successor_id)
                self.__add_edge(type_decl_id, successor_id, ENode.TypeDecl)
        pass

    def __add_local_in_file(self, file_id):
        precursors = _find_precursors(file_id, self.reader.edge_source_file)
        for precursor_id in precursors:
            if not self.reader.is_node_in(precursor_id, 'namespace_block'):
                continue
            np_id = precursor_id
            np_attrs = self.reader.type_nodes_dict['namespace_block'][np_id]
            if 'NAME' in np_attrs and np_attrs['NAME'] == '<global>':
                np_success = _find_successors(precursor_id, self.reader.edge_ast)
                for np_succ_id in np_success:
                    if not self.reader.is_node_in(np_succ_id, 'type_decl'):
                        continue
                    td_id = np_succ_id
                    td_attrs = self.reader.type_nodes_dict['type_decl'][td_id]
                    if 'NAME' in td_attrs and td_attrs['NAME'] == '<global>':
                        gtd_success = _find_successors(np_succ_id, self.reader.edge_ast)
                        for gtd_succ_id in gtd_success:
                            if not self.reader.is_node_in(gtd_succ_id, 'method'):
                                continue
                            md_id = gtd_succ_id
                            md_attrs = self.reader.type_nodes_dict['method'][md_id]
                            if 'NAME' in md_attrs and md_attrs['NAME'] == '<global>':
                                local_nodes = []
                                md_filename = md_attrs['FILENAME']
                                md_success = _find_successors(md_id, self.reader.edge_contain)
                                for md_succ_id in md_success:
                                    if not self.reader.is_node_in(md_succ_id, 'block'):
                                        continue
                                    bl_id = md_succ_id
                                    bl_success = _find_successors(bl_id, self.reader.edge_ast)
                                    for bl_succ_id in bl_success:
                                        if self.reader.is_node_in(bl_succ_id, 'local'):
                                            lo_id = bl_succ_id
                                            attributes = self.reader.type_nodes_dict['local'][lo_id]
                                            local_nodes.append((bl_succ_id, attributes))
                                for ast_node_id, attributes in local_nodes:
                                    flag = True
                                    type_decl_ids = self.index.find_items_in_file(md_filename)
                                    for type_decl_id in type_decl_ids:
                                        if self.index.find_item_in_type_decl(attributes['NAME'],
                                                                             type_decl_id) is not None:
                                            flag = False
                                            break
                                    if flag:
                                        self.__add_local_node(ast_node_id, attributes, md_filename)
        pass

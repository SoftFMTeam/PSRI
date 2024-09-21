from loguru import logger

from ccft.core.constant import ENode, ERelation, EnumNone


class NetworkxIndex:

    def __init__(self):
        self.__nodes: set[int] = set()

        self.__node_type_dict: dict[ENode, set[int]] = {
            ENode.File: set(),
            ENode.TypeDecl: set(),
            ENode.Method: set(),
            ENode.Member: set(),
            ENode.Local: set(),
        }
        ''' { node type enum : {node id} } '''

        self.__node_fullname_dict: dict[int, str] = dict()
        ''' { node id : full name }'''

        self.__fullname_node_dict: dict[str, set[int]] = dict()
        ''' { full name : {node id} }'''

        self.__signature_node_dict: dict[str, set[int]] = dict()
        ''' { method signature : {method id} }'''

        self.__node_type_fullname_dict: dict[ENode, dict[str, set[int]]] = {
            ENode.TypeDecl: dict(),
            ENode.Method: dict(),
            ENode.Member: dict(),
            ENode.Local: dict(),
        }
        ''' { node type enum : { full name : {node id} } }'''

        self.__filename_type_decl_dict: dict[str, set[int]] = dict()
        ''' { filename : { type decl id } '''

        self.__type_decl_items: dict[int, set[int]] = dict()
        ''' { type decl id : { item id } } '''

        self.__type_decl_inner_type_decls: dict[int, set[int]] = dict()
        ''' { type decl id : { inner type decl id } }'''

        self.__item_type_decl: dict[int, int] = dict()
        ''' { item id : type decl id } '''

        self.__multi_edge_r_keys: dict[ERelation, set[tuple[int, int, int]]] = {
            ERelation.Call: set(),
            ERelation.Control: set(),
            ERelation.Data: set(),
            ERelation.Contain: set(),
            ERelation.Value: set(),
            ERelation.Return: set()
        }
        ''' { edge relation enum : (source, target, key) } '''

        self.__multi_edge_r_labels: dict[str, set[tuple[int, int, int]]] = {
            'call_method': set(),
            'call_member': set(),
            'call_local': set(),

            'control_member': set(),
            'control_local': set(),
            'control_method': set(),

            'data_method': set(),

            'return_method': set(),

            'value_member': set(),
            'value_local': set(),

            'contain_type_decl': set(),
            'contain_method': set(),
            'contain_member': set(),
            'contain_local': set(),
        }
        ''' { edge relation label : (source, target, key)) }'''

        self.__type_id_to_alias_type: dict[int, set[str]] = dict()
        """ { source type id : {alias type name} } """

        self.__type_name_to_alias_type: dict[str, tuple[int, str]] = dict()
        """ { source type name : [source id, alias type name] } """

        self.__alias_type_to_type_name: dict[str, tuple[int, str]] = dict()
        """ { alias type name : [source id, source type name] } """

    def get_node_type(self, node_id, str_type: bool = False) -> None or int or tuple[int | str]:
        if self.is_node_in(node_id, ENode.File):
            if str_type:
                return ENode.File, 'file'
            return ENode.File
        elif self.is_node_in(node_id, ENode.TypeDecl):
            if str_type:
                return ENode.TypeDecl, 'type_decl'
            return ENode.TypeDecl
        elif self.is_node_in(node_id, ENode.Method):
            if str_type:
                return ENode.Method, 'method'
            return ENode.Method
        elif self.is_node_in(node_id, ENode.Member):
            if str_type:
                return ENode.Member, 'member'
            return ENode.Member
        elif self.is_node_in(node_id, ENode.Local):
            if str_type:
                return ENode.Local, 'local'
            return ENode.Local

        return None

    def is_node_in(self, node_id: int, node_type: ENode) -> bool:
        if node_type in self.__node_type_dict and node_id in self.__node_type_dict[node_type]:
            return True

        return False

    def is_node_not_in(self, node_id: int, node_type: ENode) -> bool:
        if node_id not in self.__nodes:
            return False

        return not self.is_node_in(node_id, node_type)

    def add_sub_struct(self, type_decl_id: int, sub_type_decl_id: int):
        if type_decl_id in self.__type_decl_inner_type_decls:
            self.__type_decl_inner_type_decls[type_decl_id].add(sub_type_decl_id)
        else:
            self.__type_decl_inner_type_decls[type_decl_id] = {sub_type_decl_id}
        pass

    def set_node(self, node_id: int, node_type: ENode, node_attr: dict):
        self.__nodes.add(node_id)

        if node_type == ENode.File:
            self.__node_type_dict[ENode.File].add(node_id)
        elif node_type == ENode.TypeDecl:
            self.__node_type_dict[ENode.TypeDecl].add(node_id)
        elif node_type == ENode.Method:
            self.__node_type_dict[ENode.Method].add(node_id)
        elif node_type == ENode.Member:
            self.__node_type_dict[ENode.Member].add(node_id)
        elif node_type == ENode.Local:
            self.__node_type_dict[ENode.Local].add(node_id)

        if node_type == ENode.Method and 'signature' in node_attr:
            signature = node_attr['signature']
            if isinstance(signature, str):
                if signature in self.__signature_node_dict:
                    self.__signature_node_dict[signature].add(node_id)
                else:
                    self.__signature_node_dict[signature] = {node_id}

        if 'fullname' in node_attr:
            fullname = node_attr['fullname']
            if isinstance(fullname, str):
                self.__node_fullname_dict[node_id] = fullname

                if fullname in self.__fullname_node_dict:
                    self.__fullname_node_dict[fullname].add(node_id)
                else:
                    self.__fullname_node_dict[fullname] = {node_id}

                if node_type in self.__node_type_fullname_dict:
                    t_dict = self.__node_type_fullname_dict[node_type]
                    if fullname in t_dict:
                        t_dict[fullname].add(node_id)
                    else:
                        t_dict[fullname] = {node_id}
                else:
                    self.__node_type_fullname_dict[node_type] = {fullname: {node_id}}

        if node_type == ENode.TypeDecl and 'filename' in node_attr:
            filename = node_attr['filename']
            if isinstance(filename, str):
                if filename not in self.__filename_type_decl_dict:
                    self.__filename_type_decl_dict[filename] = {node_id}
                else:
                    self.__filename_type_decl_dict[filename].add(node_id)
        pass

    def set_edge(self, source_id: int, target_id: int, r_key: ERelation, r_label: str, multi_key: int):
        if r_key in self.__multi_edge_r_keys:
            self.__multi_edge_r_keys[r_key].add((source_id, target_id, multi_key))
        else:
            # fixme relation label error
            logger.error(f'edge ({source_id}, {target_id}) relation key {r_label} error')

        if r_label in self.__multi_edge_r_labels:
            self.__multi_edge_r_labels[r_label].add((source_id, target_id, multi_key))
        else:
            logger.error(f'edge ({source_id}, {target_id}) relation label {r_label} error')

        if r_key == ERelation.Contain and source_id in self.__node_type_dict[ENode.TypeDecl]:
            if source_id in self.__type_decl_items:
                self.__type_decl_items[source_id].add(target_id)
            else:
                self.__type_decl_items[source_id] = {target_id}

            self.__item_type_decl[target_id] = source_id

    def get_nodes(self, etp: ENode) -> list[int]:
        if etp in self.__node_type_dict:
            return list(self.__node_type_dict[etp])
        return []

    def find_nodes(self, **kwargs) -> list[int]:
        etp = kwargs.get('etp')
        type_decl = kwargs.get('type_decl')
        file = kwargs.get('file')

        if 'fullname' in kwargs:
            return self.__find_nodes_by_fullname(kwargs['fullname'], etp, type_decl, file)
        elif 'header_fullname' in kwargs:
            return self.__find_nodes_by_fullname(kwargs['header_fullname'], etp, type_decl, file, True)
        elif 'signature' in kwargs:
            return self.__find_method_by_signature(kwargs['signature'])

        return []

    def find_first_or_default_node(self, **kwargs) -> int | None:
        nodes = self.find_nodes(**kwargs)
        if nodes:
            return nodes[0]
        return None

    def find_item_in_type_decl(self, keyword: str, type_decl: int | list, etp: ENode = None):
        if not isinstance(keyword, str):
            keyword = str(keyword)

        keyword = keyword.rstrip('*').rstrip('&').rstrip('(').rstrip(')')
        keyword = f'.{keyword}'

        if isinstance(type_decl, int):
            return self.__find_item_in_type_decl(keyword, type_decl, etp)
        else:
            for type_decl_id in type_decl:
                item_id = self.__find_item_in_type_decl(keyword, type_decl_id, etp)
                if item_id:
                    return item_id

        return None

    def find_type_decl_by_item(self, item_id: int):
        if item_id in self.__item_type_decl:
            return self.__item_type_decl[item_id]

        return None

    def find_items_in_file(self, filename: str) -> list[int]:
        if not isinstance(filename, str):
            filename = str(filename)

        if filename in self.__filename_type_decl_dict:
            return list(self.__filename_type_decl_dict[filename])

        return []

    def get_alias_by_fullname(self, fullname: str) -> tuple[int | None, str | None]:
        fullname = fullname.rstrip('*').rstrip('&')
        if fullname in self.__type_name_to_alias_type:
            return self.__type_name_to_alias_type[fullname]
        return None, None

    def get_source_by_alias_type(self, alias_type_name: str) -> tuple[int | None, str | None]:
        type_id = None
        type_name = None

        alias_type_name = alias_type_name.rstrip('*').rstrip('&')

        if alias_type_name in self.__alias_type_to_type_id:
            type_id = self.__alias_type_to_type_id[alias_type_name]
        if alias_type_name in self.__alias_type_to_type_name:
            type_name = self.__alias_type_to_type_name[alias_type_name]

        return type_id, type_name

    def set_alias_type_name(self, source_id: int, source_name: str, alias_type_name: str):
        if source_id not in self.__type_id_to_alias_type:
            self.__type_id_to_alias_type[source_id] = {alias_type_name}
        else:
            self.__type_id_to_alias_type[source_id].add(alias_type_name)

        if source_name not in self.__type_name_to_alias_type:
            self.__type_name_to_alias_type[source_name] = (source_id, alias_type_name)
        else:
            logger.error(f'Rename exception，{source_name} has been renamed as {self.__type_name_to_alias_type[source_name]}')

        if alias_type_name not in self.__alias_type_to_type_name:
            self.__alias_type_to_type_name[alias_type_name] = (source_id, source_name)
        else:
            logger.error(f'Rename exception，{alias_type_name} has been {self.__alias_type_to_type_name[alias_type_name]} renamed')

    def find_multi_edges(self, **kwargs):
        if 'r_key' in kwargs:
            return list(self.__multi_edge_r_keys[kwargs['r_key']])
        elif 'r_label' in kwargs:
            return list(self.__multi_edge_r_labels[kwargs['r_label']])

        return []

    def __find_method_by_signature(self, signature: str):
        if not isinstance(signature, str):
            signature = str(signature)

        nodes = []
        if signature in self.__signature_node_dict:
            nodes.extend(self.__signature_node_dict[signature])
        else:
            for k_signature, v_nodes in self.__signature_node_dict.items():
                if k_signature.endswith(signature):
                    nodes.extend(v_nodes)

        return nodes

    def __find_nodes_by_fullname(self, fullname: str, etp: ENode, type_decl: int, file: str, header=False) -> list[int]:
        if not isinstance(fullname, str):
            fullname = str(fullname)
        fullname = fullname.replace('*', '')
        fullname = fullname.replace('&', '')
        fullname = fullname.replace('(', '')
        fullname = fullname.replace(')', '')

        nodes = []
        query_list = None

        if type_decl is not None and type_decl in self.__type_decl_items:
            query_list = self.__type_decl_items[type_decl]
        elif file is not None and file in self.__filename_type_decl_dict:
            query_list = self.__filename_type_decl_dict[file]

        if query_list is not None:
            for query_id in query_list:
                t_fullname = self.__node_fullname_dict[query_id]
                if t_fullname.endswith(fullname):
                    if etp is None or etp == EnumNone:
                        nodes.append(query_id)
                    elif self.is_node_in(query_id, etp):
                        nodes.append(query_id)

        if len(nodes) == 0:
            if etp is None or etp == EnumNone:
                if fullname in self.__fullname_node_dict:
                    nodes.extend(self.__fullname_node_dict[fullname])
                else:
                    if header:
                        for k_fullname, v_nodes in self.__fullname_node_dict.items():
                            k_fullname = f'.{k_fullname}'
                            if fullname.endswith(k_fullname):
                                nodes.extend(v_nodes)
                    else:
                        fullname = f'.{fullname}'
                        for k_fullname, v_nodes in self.__fullname_node_dict.items():
                            if k_fullname.endswith(fullname):
                                nodes.extend(v_nodes)
            else:
                t_dict = self.__node_type_fullname_dict[etp]
                if fullname in t_dict:
                    nodes.extend(t_dict[fullname])
                else:
                    if header:
                        for k_fullname, v_nodes in t_dict.items():
                            k_fullname = f'.{k_fullname}'
                            if fullname.endswith(k_fullname):
                                nodes.extend(v_nodes)
                    else:
                        fullname = f'.{fullname}'
                        for k_fullname, v_nodes in t_dict.items():
                            if k_fullname.endswith(fullname):
                                nodes.extend(v_nodes)

        return nodes

    def __find_item_in_type_decl(self, item_keyword: str, type_decl: int, etp: ENode = None):
        if type_decl in self.__type_decl_items:
            items = self.__type_decl_items[type_decl]
            if type_decl in self.__type_decl_inner_type_decls:
                for sub_type_decl_id in self.__type_decl_inner_type_decls[type_decl]:
                    if sub_type_decl_id in self.__type_decl_items:
                        items = set.union(items, self.__type_decl_items[sub_type_decl_id])
            for item in items:
                if item not in self.__node_fullname_dict:
                    continue

                signature = self.__node_fullname_dict[item]
                if signature.endswith(item_keyword):
                    if etp is None or etp == EnumNone:
                        return item
                    elif self.is_node_in(item, etp):
                        return item
        return None

def _is_file(attributes: dict) -> bool:
    if ('NAME' in attributes and not attributes['NAME'].startswith('<')
            and not attributes['NAME'].endswith('>')):
        return True
    return False


def _is_type_decl(attributes: dict) -> bool:
    if ('IS_EXTERNAL' in attributes and not attributes['IS_EXTERNAL']
            and 'NAME' in attributes and attributes['NAME'] != '<global>'):
        return True
    return False


def _is_method(attributes: dict) -> bool:
    if ('IS_EXTERNAL' in attributes and not attributes['IS_EXTERNAL']
            and 'NAME' in attributes and attributes['NAME'] != '<global>'
            and 'CODE' in attributes and attributes['CODE'] != '<global>'
            and attributes['CODE'] != '<empty>'):
        return True
    return False


def _is_member(attributes: dict) -> bool:
    if 'NAME' in attributes and 'CODE' in attributes:
        return True
    return False


def _is_local(attributes: dict) -> bool:
    if 'NAME' in attributes and 'LABEL' in attributes and 'CODE' in attributes \
            and attributes['LABEL'] == 'LOCAL':
        return True
    return False


def _find_precursors(target, edges: tuple[dict[int, set], dict[int, set]], reverse: bool = False) -> list[int]:
    if target in edges[1]:
        edges = list((edges[1])[target])
        edges.sort(reverse=reverse)
        return edges
    return []


def _find_successors(source, edges: tuple[dict[int, set], dict[int, set]], reverse: bool = False) -> list[int]:
    if source in edges[0]:
        successors = list((edges[0])[source])
        successors.sort(reverse=reverse)
        return successors
    return []


def _get_successor_tree(start_id, edges: tuple[dict[int, set], dict[int, set]]) -> list[tuple[int, list[int]]]:
    visited = set()
    stack = [start_id]

    tree = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        successors = _find_successors(node, edges)
        stack.extend(successors)
        if len(successors):
            tree.append((node, successors))

    return tree

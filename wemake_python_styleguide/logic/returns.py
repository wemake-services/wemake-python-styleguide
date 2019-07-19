import ast
from collections import defaultdict
from typing import Dict, List, Tuple

NamesAndReturns = Tuple[
    Dict[str, List[ast.Name]],
    Dict[str, ast.Return]
]


def get_assign_node_variables(node: List[ast.AST]) -> List[str]:
    assign = []
    for sub_node in node:
        if isinstance(sub_node, ast.Assign):
            if isinstance(sub_node.targets[0], ast.Name):
                assign.append(sub_node.targets[0].id)
        if isinstance(sub_node, ast.AnnAssign):
            if isinstance(sub_node.target, ast.Name):
                assign.append(sub_node.target.id)
    return assign


def get_name_nodes_variable(node: List[ast.AST]) -> Dict[str, List[ast.Name]]:
    names: Dict[str, List[ast.Name]] = defaultdict(list)
    for sub_node in node:
        if isinstance(sub_node, ast.Name):
            if isinstance(sub_node.ctx, ast.Load):
                names[sub_node.id].append(sub_node)
        if isinstance(sub_node, ast.AugAssign):
            if isinstance(sub_node.target, ast.Name):
                variable_name = sub_node.target.id
                names[variable_name].append(sub_node.target)
    return names


def get_return_node_variables(node: List[ast.AST]) -> NamesAndReturns:
    returns: Dict[str, List[ast.Name]] = defaultdict(list)
    return_sub_nodes: Dict[str, ast.Return] = defaultdict()
    for sub_node in node:
        if isinstance(sub_node, ast.Return):
            if isinstance(sub_node.value, ast.Name):
                variable_name = sub_node.value.id
                returns[variable_name].append(sub_node.value)
                return_sub_nodes[variable_name] = sub_node
    return returns, return_sub_nodes

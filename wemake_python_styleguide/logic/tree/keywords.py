import ast
from typing import List, Tuple

from wemake_python_styleguide.logic.nodes import get_context


def returning_nodes(
    node: ast.AST,
    returning_type,
) -> Tuple[List[ast.Return], bool]:
    """Returns ``return`` or ``yield`` nodes with values."""
    returns: List[ast.Return] = []
    has_values = False
    for sub_node in ast.walk(node):
        context_node = get_context(sub_node)
        if isinstance(sub_node, returning_type) and context_node == node:
            if sub_node.value:
                has_values = True
            returns.append(sub_node)
    return returns, has_values


def node_returns_bool_constant(node: ast.stmt) -> bool:
    """Checks if a Return node would return a bool constant."""
    is_return = isinstance(node, ast.Return)
    if is_return:
        return_value = getattr(node, 'value')
        returns_constant = isinstance(return_value, ast.Constant)
        if returns_constant:
            constant_value = getattr(return_value, 'value')
            return isinstance(constant_value, bool)
    return False

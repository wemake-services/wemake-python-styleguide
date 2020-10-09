import ast
from typing import List, Sequence, Tuple

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


def node_returns_bool_const(node: ast.stmt) -> bool:
    """Checks if a Return node would return a boolean constant."""
    is_return = isinstance(node, ast.Return)
    if is_return:
        return_value = getattr(node, 'value', None)
        if isinstance(return_value, ast.NameConstant):
            return isinstance(return_value.value, bool)
    return False


def is_simple_return(body: Sequence[ast.stmt]) -> bool:
    """Check if a statement only returns a boolean constant."""
    if len(body) != 1:
        return False
    return node_returns_bool_const(body[0])


def next_node_returns_bool(body: Sequence[ast.stmt], index: int) -> bool:
    """Check if the node after exiting the context returns a boolean const."""
    if len(body) < index + 1:
        return False
    return node_returns_bool_const(body[index])

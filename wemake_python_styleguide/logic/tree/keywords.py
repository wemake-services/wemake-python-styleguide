import ast
from typing import List, Sequence, Tuple, Type, Union

from wemake_python_styleguide.logic.nodes import get_context

_ReturningNodes = List[Union[ast.Return, ast.Yield]]


def returning_nodes(
    node: ast.AST,
    returning_type: Union[Type[ast.Return], Type[ast.Yield]],
) -> Tuple[_ReturningNodes, bool]:
    """Returns ``return`` or ``yield`` nodes with values."""
    returns: _ReturningNodes = []
    has_values = False
    for sub_node in ast.walk(node):
        context_node = get_context(sub_node)
        if isinstance(sub_node, returning_type) and context_node == node:
            if sub_node.value:  # type: ignore
                has_values = True
            returns.append(sub_node)  # type: ignore
    return returns, has_values


def is_simple_return(body: Sequence[ast.stmt]) -> bool:
    """Check if a statement only returns a boolean constant."""
    if len(body) != 1:
        return False
    return _node_returns_bool_const(body[0])


def next_node_returns_bool(body: Sequence[ast.stmt], index: int) -> bool:
    """Check if the node after exiting the context returns a boolean const."""
    if len(body) < index + 1:
        return False
    return _node_returns_bool_const(body[index])


def _node_returns_bool_const(node: ast.stmt) -> bool:
    """Checks if a Return node would return a boolean constant."""
    return (
        isinstance(node, ast.Return) and
        isinstance(node.value, ast.NameConstant) and
        isinstance(node.value.value, bool)
    )

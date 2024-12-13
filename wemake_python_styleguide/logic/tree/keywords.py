import ast
from typing import TypeAlias

from wemake_python_styleguide.logic.nodes import get_context

_ReturningNodes: TypeAlias = list[ast.Return | ast.Yield]


def returning_nodes(
    node: ast.AST,
    returning_type: type[ast.Return] | type[ast.Yield],
) -> tuple[_ReturningNodes, bool]:
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

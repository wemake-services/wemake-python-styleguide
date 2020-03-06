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

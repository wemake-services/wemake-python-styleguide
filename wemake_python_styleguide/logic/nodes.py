import ast
from typing import Optional, Union

from wemake_python_styleguide.logic.safe_eval import literal_eval_with_names
from wemake_python_styleguide.types import ContextNodes


def is_literal(node: ast.AST) -> bool:
    """
    Checks for nodes that contains only constants.

    If the node contains only literals it will be evaluated.
    When node relies on some other names, it won't be evaluated.
    """
    try:
        ast.literal_eval(node)
    except ValueError:
        return False
    return True


def get_parent(node: ast.AST) -> Optional[ast.AST]:
    """Returns the parent node or ``None`` if node has no parent."""
    return getattr(node, 'wps_parent', None)


def get_context(node: ast.AST) -> Optional[ContextNodes]:
    """Returns the context or ``None`` if node has no context."""
    return getattr(node, 'wps_context', None)


def evaluate_node(node: ast.AST) -> Optional[Union[int, float, str, bytes]]:
    """Returns the value of a node or its evaluation."""
    if isinstance(node, ast.Name):
        return None
    if isinstance(node, (ast.Str, ast.Bytes)):
        return node.s
    try:
        signed_node = literal_eval_with_names(node)
    except Exception:
        return None
    return signed_node

import ast
from typing import Optional

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
    else:
        return True


def get_parent(node: ast.AST) -> Optional[ast.AST]:
    """Returns the parent node or ``None`` if node has no parent."""
    return getattr(node, 'wps_parent', None)


def get_context(node: ast.AST) -> Optional[ContextNodes]:
    """Returns the context or ``None`` if node has no context."""
    return getattr(node, 'wps_context', None)

# -*- coding: utf-8 -*-

import ast
from typing import Optional, Union

from wemake_python_styleguide.types import AnyNodes


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


def is_contained(node: ast.AST, to_check: Union[AnyNodes, type]) -> bool:
    """Checks whether node does contain given subnode types."""
    for child in ast.walk(node):
        if isinstance(child, to_check):
            return True
    return False


def is_doc_string(node: ast.stmt) -> bool:
    """
    Tells whether or not the given node is a docstring.

    We call docstrings any string nodes that are placed right after
    function, class, or module definition.
    """
    if not isinstance(node, ast.Expr):
        return False
    return isinstance(node.value, ast.Str)


def get_parent(node: ast.AST) -> Optional[ast.AST]:
    """Returns the parent node or ``None`` if node has no parent."""
    return getattr(node, 'wps_parent', None)

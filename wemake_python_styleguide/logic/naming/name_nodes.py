# -*- coding: utf-8 -*-

import ast
from typing import Optional


def is_same_variable(left: ast.AST, right: ast.AST) -> bool:
    """Ensures that nodes are the same variable."""
    if isinstance(left, ast.Name) and isinstance(right, ast.Name):
        return left.id == right.id
    return False


def get_assigned_name(node: ast.AST) -> Optional[str]:
    """
    Returns variable names for node that is just assigned.

    Returns ``None`` for nodes that are used in a different manner.
    """
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
        return node.id

    if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
        return node.attr

    if isinstance(node, ast.ExceptHandler):
        return getattr(node, 'name', None)

    return None

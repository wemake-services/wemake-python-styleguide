# -*- coding: utf-8 -*-

import ast
from typing import List, Optional


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


def get_variables_from_node(node: ast.AST) -> List[str]:
    """Gets the assigned names from the list of nodes."""
    names: List[str] = []
    naive_attempt = _extract_name(node)

    if naive_attempt:
        names.append(naive_attempt)
    elif isinstance(node, ast.Tuple):
        for subnode in node.elts:
            extracted_name = _extract_name(subnode)
            if extracted_name:
                names.append(extracted_name)
    return names


def _extract_name(node: ast.AST) -> Optional[str]:
    """
    Utility to extract names for several types of nodes.

    Should not be used direclty, use safer :py:`~get_assign_names` function.
    """
    if isinstance(node, ast.Starred):
        node = node.value
    if isinstance(node, ast.Name):
        return node.id
    return None

# -*- coding: utf-8 -*-

import ast
from typing import Optional


def unwrap_unary_node(node: ast.AST) -> ast.AST:
    """
    Returns a real unwrapped node from the unary wrapper.

    It recursively unwraps any level of unary operators.
    Returns the node itself if it is not wrapped in unary operator.
    """
    if not isinstance(node, ast.UnaryOp):
        return node
    return unwrap_unary_node(node.operand)


def get_parent_ignoring_unary(node: ast.AST) -> Optional[ast.AST]:
    """
    Returns real parent ignoring proxy unary parent level.

    What can go wrong?

    1. Number can be negative: ``x = -1``,
       so ``1`` has ``UnaryOp`` as parent, but should return ``Assign``
    2. Some values can be negated: ``x = --some``,
       so ``some`` has ``UnaryOp`` as parent, but should return ``Assign``

    """
    parent = getattr(node, 'wps_parent', None)
    if parent is None or not isinstance(parent, ast.UnaryOp):
        return parent
    return get_parent_ignoring_unary(parent)

# -*- coding: utf-8 -*-

import ast
from typing import Union

_VarDefinition = Union[ast.AST, ast.expr]


def _is_valid_single(node: _VarDefinition) -> bool:
    if isinstance(node, ast.Name):
        return True
    if isinstance(node, ast.Starred) and isinstance(node.value, ast.Name):
        return True
    return False


def is_valid_block_variable_definition(node: _VarDefinition) -> bool:
    """Is used to check either block variables are correctly defined."""
    if isinstance(node, ast.Tuple):
        for var_definition in node.elts:
            if not _is_valid_single(var_definition):
                return False
        return True
    return _is_valid_single(node)

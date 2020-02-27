# -*- coding: utf-8 -*-

import ast
from typing import Set, Union

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


def name_in_postfix(
    node: ast.ClassDef,
    names: Set[str],
    postfixes: Set[str],
) -> bool:
    """Checks if name is in any postfix."""
    for postfix in postfixes:
        if any(name == postfix for name in names):
            return True
    return False

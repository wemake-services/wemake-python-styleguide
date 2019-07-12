# -*- coding: utf-8 -*-

import ast
from typing import Union

VarDefinition = Union[ast.AST, ast.expr]


def is_valid_block_variable_definition(node: VarDefinition) -> bool:
    """Is used to check either block variables are correctly defined."""
    if isinstance(node, ast.Name):
        return True

    if isinstance(node, ast.Tuple):
        for var_definition in node.elts:
            if not isinstance(var_definition, ast.Name):
                return False
        return True
    return False

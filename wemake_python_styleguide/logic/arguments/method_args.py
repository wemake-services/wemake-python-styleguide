# -*- coding: utf-8 -*-

import ast
from typing import List

from wemake_python_styleguide import types


def get_args_without_self(node: types.AnyFunctionDefAndLambda) -> List[ast.arg]:
    """Gets ``node`` arguments excluding ``self``."""
    node_args = node.args.args
    if not node_args or isinstance(node, ast.Lambda):
        return node_args
    if node_args[0].arg != 'self':
        return node_args
    return node_args[1:]

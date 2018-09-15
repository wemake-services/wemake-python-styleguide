# -*- coding: utf-8 -*-

import ast
from typing import Iterable, Type


def is_subtype_of_any(
    node: ast.AST,
    to_check: Iterable[Type[ast.AST]],
) -> bool:
    """
    Checks either the given node is subtype of any of the provided types.

    >>> import ast
    >>> node = ast.parse('')  # ast.Module
    >>> is_subtype_of_any(node, [ast.Str, ast.Name])
    False

    >>> is_subtype_of_any(node, [ast.Module])
    True

    >>> is_subtype_of_any(node, [])
    False

    """
    return any(isinstance(node, class_) for class_ in to_check)

# -*- coding: utf-8 -*-

import ast
from typing import Iterable, Optional


def _chained_item(iterator: ast.AST) -> Optional[ast.Call]:
    if isinstance(iterator, ast.Call):
        for child in ast.iter_child_nodes(iterator):
            if isinstance(child, ast.Call):
                return iterator
    elif (isinstance(iterator, ast.Expr) and
            isinstance(iterator.value, ast.Call)):
        return iterator.value
    return None


def parts(node: ast.Call) -> Iterable[ast.Call]:
    """Returns all consecutive function calls."""
    iterator: ast.Call = node

    while True:
        yield iterator

        chained_item = _chained_item(iterator)
        if chained_item is None:
            return
        iterator = chained_item

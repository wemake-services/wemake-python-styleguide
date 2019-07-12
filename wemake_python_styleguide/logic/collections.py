# -*- coding: utf-8 -*-

import ast
from typing import List, Sequence


def normalize_dict_elements(node: ast.Dict) -> Sequence[ast.AST]:
    """
    Normalizes ``dict`` elements and enforces consistent order.

    We had a problem that some ``dict`` objects might not have some keys.

    Example::

        some_dict = {**one, **two}

    This ``dict`` contains two values and zero keys.
    This function will normalize this structure to use
    values instead of missing keys.

    See also:
        https://github.com/wemake-services/wemake-python-styleguide/issues/450

    """
    elements: List[ast.AST] = []
    for dict_key, dict_value in zip(node.keys, node.values):
        if dict_key is None:
            elements.append(dict_value)  # type: ignore
        else:
            elements.append(dict_key)
    return elements

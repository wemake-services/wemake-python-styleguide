# -*- coding: utf-8 -*-

import ast


def is_literal(node: ast.AST) -> bool:
    """
    Checks for nodes that contains only constants.

    If the node contains only literals it will be evaluated.
    When node relies on some other names, it won't be evaluated.
    """
    try:
        ast.literal_eval(node)
    except ValueError:
        return False
    else:
        return True

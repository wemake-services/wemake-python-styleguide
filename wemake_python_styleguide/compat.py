# -*- coding: utf-8 -*-

"""
This module contains ugly hacks and fixes for version compat issues.

Do not be over-exited to add anything here.
"""

import ast


def maybe_set_parent(tree: ast.AST) -> ast.AST:
    """Sets parents for all nodes that do not have this prop."""
    for statement in ast.walk(tree):
        for child in ast.iter_child_nodes(statement):
            if not hasattr(child, 'parent'):  # noqa: Z113
                setattr(child, 'parent', statement)  # noqa: Z113

    return tree

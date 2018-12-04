# -*- coding: utf-8 -*-

import ast


def fix_async_offset(tree: ast.AST) -> ast.AST:
    """
    Fixes ``col_offest`` values for async nodes.

    This is a temporary check for async-based expressions, because offset
    for them isn't calculated properly. We can calculate right version
    of offset with subscripting ``6`` (length of "async " part).

    Affected ``python`` versions:

    - all versions below ``python3.6.7``

    Read more:
        https://bugs.python.org/issue29205
        https://github.com/wemake-services/wemake-python-styleguide/issues/282

    """
    nodes_to_fix = (
        ast.AsyncFor,
        ast.AsyncWith,
        ast.AsyncFunctionDef,
    )
    for node in ast.walk(tree):
        if isinstance(node, nodes_to_fix):
            error = 6 if node.col_offset % 4 != 0 else 0
            node.col_offset = node.col_offset - error
    return tree


def fix_line_number(tree: ast.AST) -> ast.AST:
    """
    Adjusts line number for some nodes.

    They are set incorrectly for some collections.
    It might be either a bug or a feature.

    We do several checks here, to be sure that we won't get
    an incorrect line number. But, we basically check if there's
    a parent, so we can compare and adjust.

    Example::

        print((  # should start from here
            1, 2, 3,  # actually starts from here
        ))

    """
    affected = (ast.Tuple,)
    for node in ast.walk(tree):
        if isinstance(node, affected):
            parent_lineno = getattr(
                getattr(node, 'parent', None), 'lineno', None,
            )
            if parent_lineno and parent_lineno < node.lineno:
                node.lineno = node.lineno - 1
    return tree

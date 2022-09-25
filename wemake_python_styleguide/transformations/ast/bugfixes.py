import ast

from wemake_python_styleguide.logic.nodes import get_parent


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
            parent_lineno = getattr(get_parent(node), 'lineno', None)
            if parent_lineno and parent_lineno < node.lineno:
                node.lineno = node.lineno - 1
    return tree

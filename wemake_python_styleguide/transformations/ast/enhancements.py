# -*- coding: utf-8 -*-

import ast
from typing import Optional, Tuple, Type

from wemake_python_styleguide.compat.aliases import FunctionNodes


def set_if_chain(tree: ast.AST) -> ast.AST:
    """
    Used to create ``if`` chains.

    We have a problem, because we can not tell which situation is happening:

    .. code:: python

        if some_value:
            if other_value:
                ...

    .. code:: python

        if some_value:
            ...
        elif other_value:
            ...

    Since they are very similar it very hard to make a different when
    actually working with nodes. So, we need a simple way to separate them.
    """
    for statement in ast.walk(tree):
        for child in ast.iter_child_nodes(statement):
            if isinstance(statement, ast.If) and isinstance(child, ast.If):
                if child in statement.orelse:
                    setattr(statement, 'wps_chained', True)  # noqa: WPS425
                    setattr(child, 'wps_chain', statement)  # noqa: B010
    return tree


def set_node_context(tree: ast.AST) -> ast.AST:
    """
    Used to set proper context to all nodes.

    What we call "a context"?
    Context is where exactly this node belongs on a global level.

    Example::

        if some_value > 2:
            test = 'passed'

    Despite the fact ``test`` variable has ``Assign`` as it parent
    it will have ``Module`` as a context.

    What contexts do we respect?

    - :py:class:`ast.Module`
    - :py:class:`ast.ClassDef`
    - :py:class:`ast.FunctionDef` and :py:class:`ast.AsyncFunctionDef`

    .. versionchanged:: 0.8.1

    """
    contexts = (
        ast.Module,
        ast.ClassDef,
        *FunctionNodes,
    )

    for statement in ast.walk(tree):
        current_context = _find_context(statement, contexts)
        setattr(statement, 'wps_context', current_context)  # noqa: B010
    return tree


def _find_context(
    node: ast.AST,
    contexts: Tuple[Type[ast.AST], ...],
) -> Optional[ast.AST]:
    """
    We changed how we find and assign contexts in 0.8.1 version.

    It happened because of the bug #520
    See: https://github.com/wemake-services/wemake-python-styleguide/issues/520
    """
    parent = getattr(node, 'wps_parent', None)
    if parent is None:
        return None
    elif isinstance(parent, contexts):
        return parent
    else:
        return _find_context(parent, contexts)

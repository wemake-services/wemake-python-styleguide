# -*- coding: utf-8 -*-

import ast


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
                    setattr(statement, 'wps_chained', True)  # noqa: Z425
                    setattr(child, 'wps_chain', statement)
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

    """
    contexts = (
        ast.Module,
        ast.ClassDef,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
    )

    current_context = None
    for statement in ast.walk(tree):
        if isinstance(statement, contexts):
            current_context = statement

        for child in ast.iter_child_nodes(statement):
            setattr(child, 'wps_context', current_context)
    return tree

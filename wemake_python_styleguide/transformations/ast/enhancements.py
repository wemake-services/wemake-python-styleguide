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
                    setattr(statement, 'chained', True)  # noqa: Z425
                    setattr(child, 'chain', statement)
    return tree

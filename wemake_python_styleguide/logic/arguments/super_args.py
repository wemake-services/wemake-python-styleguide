# -*- coding: utf-8 -*-

import ast
from typing import Optional


def is_super_called_with(call: ast.Call, type_: str, object_: str) -> bool:
    """Tells whether super ``call`` was done with ``type_`` and ``object_``."""
    arg1: Optional[ast.expr] = None
    arg2: Optional[ast.expr] = None
    if len(call.args) == 2:
        #: super(Test, self)
        arg1 = call.args[0]
        arg2 = call.args[1]
    elif len(call.keywords) == 2:
        #: super(t=Test, obj=self)
        for keyword in call.keywords:
            if keyword.arg == 't':
                arg1 = keyword.value
            elif keyword.arg == 'obj':
                arg2 = keyword.value
    else:
        #: super(Test, obj=self)
        arg1 = call.args[0]
        arg2 = call.keywords[0].value
    is_expected_type = isinstance(arg1, ast.Name) and arg1.id == type_
    is_expected_object = isinstance(arg2, ast.Name) and arg2.id == object_
    return is_expected_type and is_expected_object


def is_ordinary_super_call(node: ast.AST, class_name: str) -> bool:
    """
    Tells whether super ``call`` is ordinary.

    By ordinary we mean:

    - either call without arguments::

        super().function()

    - or call with our class and self arguments::

        super(Class, self).function()

    Any other combination of arguments is considered as unordinary by
    this function.
    """
    if not isinstance(node, ast.Call):
        return False
    if not isinstance(node.func, ast.Name) or node.func.id != 'super':
        return False
    if not node.args and not node.keywords:
        return True
    if len(node.args) + len(node.keywords) != 2:
        return False
    return is_super_called_with(
        node,
        type_=class_name,
        object_='self',
    )

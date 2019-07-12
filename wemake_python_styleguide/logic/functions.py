# -*- coding: utf-8 -*-

from ast import Call, arg
from typing import Container, List, Optional

import astor

from wemake_python_styleguide.types import AnyFunctionDefAndLambda


def given_function_called(node: Call, to_check: Container[str]) -> str:
    """
    Returns function name if it is called and contained in the container.

    >>> import ast
    >>> module = ast.parse('print(123, 456)')
    >>> given_function_called(module.body[0].value, ['print'])
    'print'

    >>> given_function_called(module.body[0].value, ['adjust'])
    ''

    """
    function_name = astor.to_source(node.func).strip()
    if function_name in to_check:
        return function_name
    return ''


def is_method(function_type: Optional[str]) -> bool:
    """
    Returns whether a given function type belongs to a class.

    >>> is_method('function')
    False

    >>> is_method(None)
    False

    >>> is_method('method')
    True

    >>> is_method('classmethod')
    True

    >>> is_method('staticmethod')
    True

    >>> is_method('')
    False

    """
    return function_type in {'method', 'classmethod', 'staticmethod'}


def get_all_arguments(node: AnyFunctionDefAndLambda) -> List[arg]:
    """
    Returns list of all arguments that exist in a function.

    Respects the correct parameters order.
    Positional args, ``*args``, keyword-only, ``**kwargs``.
    """
    names = [
        *node.args.args,
        *node.args.kwonlyargs,
    ]

    if node.args.vararg:
        names.insert(len(node.args.args), node.args.vararg)

    if node.args.kwarg:
        names.append(node.args.kwarg)

    return names


def is_first_argument(node: AnyFunctionDefAndLambda, name: str) -> bool:
    """Tells whether an argument name is the logically first in function."""
    if not node.args.args:
        return False

    return name == node.args.args[0].arg

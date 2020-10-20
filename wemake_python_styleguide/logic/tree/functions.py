from ast import Call, Yield, YieldFrom, arg
from typing import Container, List, Optional

from wemake_python_styleguide.compat.functions import get_posonlyargs
from wemake_python_styleguide.logic import source
from wemake_python_styleguide.logic.walk import is_contained
from wemake_python_styleguide.types import (
    AnyFunctionDef,
    AnyFunctionDefAndLambda,
)


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
    function_name = source.node_to_string(node.func)
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
    Positional only args, regular argument,
    ``*args``, keyword-only, ``**kwargs``.

    Positional only args are only added for ``python3.8+``
    other versions are ignoring this type of arguments.
    """
    names = [
        *get_posonlyargs(node),
        *node.args.args,
    ]

    if node.args.vararg:
        names.append(node.args.vararg)

    names.extend(node.args.kwonlyargs)

    if node.args.kwarg:
        names.append(node.args.kwarg)

    return names


def is_first_argument(node: AnyFunctionDefAndLambda, name: str) -> bool:
    """Tells whether an argument name is the logically first in function."""
    positional_args = [
        *get_posonlyargs(node),
        *node.args.args,
    ]

    if not positional_args:
        return False

    return name == positional_args[0].arg


def is_generator(node: AnyFunctionDef) -> bool:
    """Tells whether a given function is a generator."""
    for body_item in node.body:
        if is_contained(node=body_item, to_check=(Yield, YieldFrom)):
            return True
    return False

# -*- coding: utf-8 -*-

from ast import Call
from typing import Iterable, Optional


def given_function_called(node: Call, to_check: Iterable[str]) -> str:
    """
    Returns function name if it is called and contained in the `to_check`.

    >>> import ast
    >>> module = ast.parse('print("some value")')
    >>> given_function_called(module.body[0].value, ['print'])
    'print'

    """
    function_name = getattr(node.func, 'id', None)
    function_value = getattr(node.func, 'value', None)
    function_inner_id = getattr(function_value, 'id', None)
    function_attr = getattr(node.func, 'attr', None)

    is_restricted_function_attribute = (
        function_inner_id in to_check and function_attr in to_check
    )

    if function_name in to_check or is_restricted_function_attribute:
        return function_name
    return ''


def is_method(function_type: Optional[str]) -> bool:
    """
    Returns either or not given function type belongs to a class.

    >>> is_method('function')
    False

    >>> is_method(None)
    False

    >>> is_method('method')
    True

    >>> is_method('classmethod')
    True

    >>> is_method('')
    False

    """
    return function_type in ['method', 'classmethod']

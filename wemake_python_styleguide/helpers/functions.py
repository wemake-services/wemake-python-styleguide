# -*- coding: utf-8 -*-

from ast import Call
from typing import Iterable


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

    is_restricted_function = function_name in to_check
    is_restricted_function_attribute = (
        function_inner_id in to_check and function_attr in to_check
    )

    if is_restricted_function or is_restricted_function_attribute:
        return function_name
    return ''

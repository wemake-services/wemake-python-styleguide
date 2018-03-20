# -*- coding: utf-8 -*-

from ast import Call
from typing import Iterable


def given_function_called(node: Call, to_check: Iterable[str]) -> str:
    function_name = getattr(node.func, 'id', None)
    function_value = getattr(node.func, 'value', None)
    function_inner_id = getattr(function_value, 'id', None)
    function_attr = getattr(node.func, 'attr', None)

    is_print_function = function_name in to_check
    is_print_function_attribute = (
       function_inner_id in to_check and
       function_attr in to_check
    )

    if is_print_function or is_print_function_attribute:
        return function_name
    return ''

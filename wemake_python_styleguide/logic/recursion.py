# -*- coding: utf-8 -*-

from ast import Call, walk

from wemake_python_styleguide.logic.functions import given_function_called
from wemake_python_styleguide.types import AnyFunctionDef


# TODO: check methods separately
def has_recursive_calls(func: AnyFunctionDef) -> bool:
    """
    Determins whether function has recrusive calls or not.

    Does not work for methods.
    """
    return bool([
        node for node in walk(func)
        if isinstance(node, Call) and given_function_called(node, {func.name})
    ])

# -*- coding: utf-8 -*-

import ast
from itertools import zip_longest
from typing import List, Optional

from wemake_python_styleguide import types


def get_args_without_self(node: types.AnyFunctionDefAndLambda) -> List[ast.arg]:
    """Gets ``node`` arguments excluding ``self``."""
    node_args = node.args.args
    if not node_args:
        return node_args
    if isinstance(node, ast.Lambda):
        return node_args
    first_arg = node_args[0]
    if first_arg.arg != 'self':
        return node_args
    return node_args[1:]


def has_same_vararg(
    node: types.AnyFunctionDefAndLambda,
    call: ast.Call,
) -> bool:
    """Tells whether ``call`` has the same vararg ``*args`` as ``node``."""
    vararg_name: Optional[str] = None
    for ar in call.args:
        # 'args': [<_ast.Starred object at 0x10d77a3c8>]
        if isinstance(ar, ast.Starred):
            if isinstance(ar.value, ast.Name):
                vararg_name = ar.value.id
            else:  # We can judge on things like `*[]`
                return False
    if vararg_name and node.args.vararg:
        return node.args.vararg.arg == vararg_name
    return node.args.vararg == vararg_name


def has_same_kwarg(node: types.AnyFunctionDefAndLambda, call: ast.Call) -> bool:
    """Tells whether ``call`` has the same kwargs as ``node``."""
    kwarg_name: Optional[str] = None
    for keyword in call.keywords:
        # `a=1` vs `**kwargs`:
        # {'arg': 'a', 'value': <_ast.Num object at 0x1027882b0>}
        # {'arg': None, 'value': <_ast.Name object at 0x102788320>}
        if keyword.arg is None:
            if isinstance(keyword.value, ast.Name):
                kwarg_name = keyword.value.id
            else:  # We can judge on things like `**{}`
                return False
    if node.args.kwarg and kwarg_name:
        return node.args.kwarg.arg == kwarg_name
    return node.args.kwarg == kwarg_name


def has_same_args(node: types.AnyFunctionDefAndLambda, call: ast.Call) -> bool:
    """Tells whether ``call`` has the same positional args as ``node``."""
    node_args = get_args_without_self(node)
    paired_arguments = zip_longest(call.args, node_args)
    for call_arg, func_arg in paired_arguments:
        if isinstance(call_arg, ast.Starred):
            if isinstance(func_arg, ast.arg):
                return False
        elif isinstance(call_arg, ast.Name):
            if not func_arg or call_arg.id != func_arg.arg:
                return False
        else:
            return False
    return True


def has_same_kw_args(
    node: types.AnyFunctionDefAndLambda,
    call: ast.Call,
) -> bool:
    """Tells whether ``call`` has the same keyword args as ``node``."""
    prepared_kw_args = {
        kw.arg: kw
        for kw in call.keywords
        if isinstance(kw.value, ast.Name) and kw.arg == kw.value.id
    }

    real_kw_args = [
        # We need to remove ** args from here:
        kw for kw in call.keywords
        if not (isinstance(kw.value, ast.Name) and kw.arg is None)
    ]

    for func_arg in node.args.kwonlyargs:
        func_arg_name = getattr(func_arg, 'arg', None)
        call_arg = prepared_kw_args.get(func_arg_name)

        if func_arg and not call_arg:
            return False
    return len(real_kw_args) == len(node.args.kwonlyargs)


def is_call_matched_by_arguments(
    node: types.AnyFunctionDefAndLambda,
    call: ast.Call,
) -> bool:
    """Tells whether ``call`` is matched by arguments of ``node``."""
    same_vararg = has_same_vararg(node, call)
    same_kwarg = has_same_kwarg(node, call)
    if not same_vararg or not same_kwarg:
        return False

    same_args = has_same_args(node, call)
    same_kw_args = has_same_kw_args(node, call)
    if not same_args or not same_kw_args:
        return False
    return True

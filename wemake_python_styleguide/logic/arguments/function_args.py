import ast
from collections.abc import Mapping
from itertools import zip_longest

from wemake_python_styleguide import types
from wemake_python_styleguide.logic.arguments.call_args import get_starred_args
from wemake_python_styleguide.logic.arguments.special_args import (
    clean_special_argument,
)


def is_call_matched_by_arguments(
    node: types.AnyFunctionDefAndLambda,
    call: ast.Call,
) -> bool:
    """Tells whether ``call`` is matched by arguments of ``node``."""
    same_args = _has_same_args(node, call)
    same_vararg = _has_same_vararg(node, call)
    same_kwarg = _has_same_kwarg(node, call)
    same_kw_args = _has_same_kw_args(node, call)
    return same_args and same_vararg and same_kwarg and same_kw_args


def get_args_without_special_argument(
    node: types.AnyFunctionDefAndLambda,
) -> list[ast.arg]:
    """Gets ``node`` arguments excluding ``self``, ``cls``, ``mcs``."""
    node_args = node.args.posonlyargs + node.args.args
    return clean_special_argument(node, node_args)


def _has_same_vararg(
    node: types.AnyFunctionDefAndLambda,
    call: ast.Call,
) -> bool:
    """Tells whether ``call`` has the same vararg ``*args`` as ``node``."""
    vararg_name: str | None = None
    for starred_arg in get_starred_args(call):
        # 'args': [<_ast.Starred object at 0x10d77a3c8>]
        if isinstance(starred_arg.value, ast.Name):
            vararg_name = starred_arg.value.id
        else:  # We can judge on things like `*[]`
            return False
    if vararg_name and node.args.vararg:
        return node.args.vararg.arg == vararg_name
    return node.args.vararg == vararg_name  # type: ignore


def _has_same_kwarg(
    node: types.AnyFunctionDefAndLambda,
    call: ast.Call,
) -> bool:
    """Tells whether ``call`` has the same kwargs as ``node``."""
    kwarg_name: str | None = None
    null_arg_keywords = filter(lambda key: key.arg is None, call.keywords)
    for keyword in null_arg_keywords:
        # `a=1` vs `**kwargs`:
        # {'arg': 'a', 'value': <_ast.Constant(1) object at 0x1027882b0>}
        # {'arg': None, 'value': <_ast.Name object at 0x102788320>}
        if isinstance(keyword.value, ast.Name):
            kwarg_name = keyword.value.id
        else:  # We can judge on things like `**{}`
            return False
    if node.args.kwarg and kwarg_name:
        return node.args.kwarg.arg == kwarg_name
    return node.args.kwarg == kwarg_name  # type: ignore


def _has_same_args(  # noqa: WPS231
    node: types.AnyFunctionDefAndLambda,
    call: ast.Call,
) -> bool:
    """Tells whether ``call`` has the same positional args as ``node``."""
    node_args = get_args_without_special_argument(node)
    paired_arguments = zip_longest(call.args, node_args)
    for call_arg, func_arg in paired_arguments:
        if isinstance(call_arg, ast.Starred):
            # nevertheless `*args` is vararg ensure there is no
            # plain arg defined on corresponding position
            if isinstance(func_arg, ast.arg):
                return False
        elif isinstance(call_arg, ast.Name):
            # for each found call arg there should be not null
            # same func arg defined on the same position
            if not func_arg or call_arg.id != func_arg.arg:
                return False
        else:
            return False
    return True


def _clean_call_keyword_args(
    call: ast.Call,
) -> tuple[Mapping[str, ast.keyword], list[ast.keyword]]:
    prepared_kw_args = {}
    real_kw_args = []
    for kw in call.keywords:
        if isinstance(kw.value, ast.Name) and kw.arg == kw.value.id:
            prepared_kw_args[kw.arg] = kw
        if not (isinstance(kw.value, ast.Name) and kw.arg is None):
            # We need to remove ** args from here:
            real_kw_args.append(kw)
    return prepared_kw_args, real_kw_args


def _has_same_kw_args(
    node: types.AnyFunctionDefAndLambda,
    call: ast.Call,
) -> bool:
    """Tells whether ``call`` has the same keyword-only args as ``node``."""
    prepared_kw_args, real_kw_args = _clean_call_keyword_args(call)
    for func_arg in node.args.kwonlyargs:
        call_arg = prepared_kw_args.get(func_arg.arg)
        if call_arg is None:
            return False
    return len(real_kw_args) == len(node.args.kwonlyargs)

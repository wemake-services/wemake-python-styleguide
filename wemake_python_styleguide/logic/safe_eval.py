# -*- coding: utf-8 -*-

from ast import (
    AST,
    Add,
    BinOp,
    Bytes,
    Dict,
    List,
    Name,
    NameConstant,
    Num,
    Set,
    Str,
    Sub,
    Tuple,
    UAdd,
    UnaryOp,
    USub,
)
from typing import Any, Optional, Union

from wemake_python_styleguide.compat.nodes import Constant


def _convert_num(node: AST):
    if isinstance(node, Constant):  # pragma: no cover
        if isinstance(node.value, (int, float, complex)):
            return node.value
    elif isinstance(node, Num):
        return node.n
    elif isinstance(node, Name):  # That's what is modified from the original
        # We return string names as is, see how we return strings:
        return node.id
    raise ValueError('malformed node or string: {0!r}'.format(node))


def _convert_signed_num(node: AST):
    if isinstance(node, UnaryOp) and isinstance(node.op, (UAdd, USub)):
        operand = _convert_num(node.operand)
        return +operand if isinstance(node.op, UAdd) else -operand
    return _convert_num(node)


def _convert_complex(node: BinOp) -> Optional[complex]:
    left = _convert_signed_num(node.left)
    right = _convert_num(node.right)
    if isinstance(left, (int, float)) and isinstance(right, complex):
        if isinstance(node.op, Add):
            return left + right
        return left - right
    return None


def _convert_iterable(node: Union[Tuple, List, Set, Dict]):
    if isinstance(node, Tuple):
        return tuple(map(literal_eval_with_names, node.elts))
    elif isinstance(node, List):
        return list(map(literal_eval_with_names, node.elts))
    elif isinstance(node, Set):
        return set(map(literal_eval_with_names, node.elts))
    return dict(zip(
        map(literal_eval_with_names, node.keys),
        map(literal_eval_with_names, node.values),
    ))


def literal_eval_with_names(node: AST) -> Optional[Any]:  # noqa: WPS231
    """
    Safely evaluate constants and ``ast.Name`` nodes.

    We need this function to tell
    that ``[name]`` and ``[name]`` are the same nodes.

    Copied from the CPython's source code.
    Modified to treat ``ast.Name`` nodes as constants.

    See: :py:`ast.literal_eval` source.

    We intentionally ignore complexity violation here,
    becase we try to stay as close to the original source as possible.
    """
    if isinstance(node, (Constant, NameConstant)):
        return node.value
    elif isinstance(node, (Str, Bytes, Num)):
        # We wrap strings to tell the difference between strings and names:
        return node.n if isinstance(node, Num) else '"{0!r}"'.format(node.s)
    elif isinstance(node, (Tuple, List, Set, Dict)):
        return _convert_iterable(node)
    elif isinstance(node, BinOp) and isinstance(node.op, (Add, Sub)):
        maybe_complex = _convert_complex(node)
        if maybe_complex is not None:
            return maybe_complex
    return _convert_signed_num(node)

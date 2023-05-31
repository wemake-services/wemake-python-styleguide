import ast
from typing import Any, Optional, Union


def _convert_num(node: Optional[ast.AST]):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float, complex)):
            return node.value
    # That's what is modified from the original
    elif isinstance(node, ast.Name):
        # We return string names as is, see how we return strings:
        return node.id
    raise ValueError('malformed node or string: {0!r}'.format(node))


def _convert_signed_num(node: Optional[ast.AST]):
    unary_operators = (ast.UAdd, ast.USub)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, unary_operators):
        operand = _convert_num(node.operand)
        return +operand if isinstance(node.op, ast.UAdd) else -operand
    return _convert_num(node)


def _convert_complex(node: ast.BinOp) -> Optional[complex]:
    left = _convert_signed_num(node.left)
    right = _convert_num(node.right)
    if isinstance(left, (int, float)) and isinstance(right, complex):
        if isinstance(node.op, ast.Add):
            return left + right
        return left - right
    return None


def _convert_iterable(node: Union[ast.Tuple, ast.List, ast.Set, ast.Dict]):
    if isinstance(node, ast.Tuple):
        return tuple(map(literal_eval_with_names, node.elts))
    elif isinstance(node, ast.List):
        return list(map(literal_eval_with_names, node.elts))
    elif isinstance(node, ast.Set):
        return set(map(literal_eval_with_names, node.elts))
    return dict(zip(
        map(literal_eval_with_names, node.keys),
        map(literal_eval_with_names, node.values),
    ))


def literal_eval_with_names(  # noqa: WPS231
    node: Optional[ast.AST],
) -> Any:
    """
    Safely evaluate constants and ``ast.Name`` nodes.

    We need this function to tell
    that ``[name]`` and ``[name]`` are the same nodes.

    Copied from the CPython's source code.
    Modified to treat ``ast.Name`` nodes as constants.

    See: :py:`ast.literal_eval` source.

    We intentionally ignore complexity violation here,
    because we try to stay as close to the original source as possible.
    """
    binary_operators = (ast.Add, ast.Sub)
    if isinstance(node, (ast.Constant, ast.NameConstant)):
        return node.value
    elif isinstance(node, (ast.Tuple, ast.List, ast.Set, ast.Dict)):
        return _convert_iterable(node)
    elif isinstance(node, ast.BinOp) and isinstance(node.op, binary_operators):
        maybe_complex = _convert_complex(node)
        if maybe_complex is not None:
            return maybe_complex
    return _convert_signed_num(node)

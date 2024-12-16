import ast

from wemake_python_styleguide.types import AnyFunctionDef


def is_stub(node: AnyFunctionDef) -> bool:
    """
    Checks if a function is a stub.

    A function (or method) is considered to be a stub if it contains:
        - only a docstring
        - only an Ellipsis statement (i.e. `...`)
        - only a `raise` statement
        - a docstring + an Ellipsis statement
        - a docstring + a `raise` statement
    """
    first_node = node.body[0]
    if (
        isinstance(first_node, ast.Expr)
        and isinstance(first_node.value, ast.Constant)
        and isinstance(first_node.value.value, str)
    ):
        return _is_stub_with_docstring(node)
    return _is_stub_without_docstring(first_node)


def _is_stub_with_docstring(node: AnyFunctionDef) -> bool:
    statements_in_body = len(node.body)
    if statements_in_body == 1:
        return True
    if statements_in_body == 2:
        second_node = node.body[1]
        return _is_ellipsis(second_node) or isinstance(second_node, ast.Raise)
    return False


def _is_stub_without_docstring(node: ast.AST) -> bool:
    return _is_ellipsis(node) or isinstance(node, ast.Raise)


def _is_ellipsis(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, type(...))
    )

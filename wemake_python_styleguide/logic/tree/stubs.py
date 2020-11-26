from ast import AST, Ellipsis, Expr, Raise, Str

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
    function_has_docstring = (
        isinstance(node.body[0], Expr) and
        isinstance(node.body[0].value, Str)
    )
    if function_has_docstring:
        return _is_stub_with_docstring(node)
    return _is_stub_without_docstring(node)


def _is_stub_with_docstring(node: AnyFunctionDef) -> bool:
    statements_in_body = len(node.body)
    if statements_in_body == 1:
        return True
    elif statements_in_body == 2:
        return (
            _is_ellipsis(node.body[1]) or
            isinstance(node.body[1], Raise)
        )
    return False


def _is_stub_without_docstring(node: AnyFunctionDef) -> bool:
    return (
        len(node.body) == 1 and
        (
            _is_ellipsis(node.body[0]) or
            isinstance(node.body[0], Raise)
        )
    )


def _is_ellipsis(node: AST) -> bool:
    return (
        isinstance(node, Expr) and
        isinstance(node.value, Ellipsis)
    )

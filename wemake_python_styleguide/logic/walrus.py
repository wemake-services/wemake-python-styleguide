import ast

from wemake_python_styleguide.compat.nodes import NamedExpr


def get_assigned_expr(node: ast.AST) -> ast.AST:
    """
    Helper function to retrieve assigned value from ``NamedExpr``.

    If the node is an actual ``NamedExpr``, the assigned value will be returned.
    For other node type, the original node is returned.

    This code is only executed on ``python3.8+``,
    because before ``3.8.0`` release
    there was no such thing as walrus or ``:=`` operator.
    """
    if isinstance(node, NamedExpr):  # pragma: py-lt-38
        return node.value
    return node

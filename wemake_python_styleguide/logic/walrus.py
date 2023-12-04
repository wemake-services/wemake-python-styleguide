import ast


def get_assigned_expr(node: ast.AST) -> ast.AST:
    """
    Helper function to retrieve assigned value from ``NamedExpr``.

    If the node is an actual ``NamedExpr``, the assigned value will be returned.
    For other node type, the original node is returned.
    """
    if isinstance(node, ast.NamedExpr):
        return node.value
    return node

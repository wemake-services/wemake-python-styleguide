import ast


def previous_node(parent: ast.AST, node: ast.AST) -> ast.AST | None:
    """Return previous node in a body of parent."""
    body: list[ast.AST] = getattr(parent, 'body', [])
    try:
        return body[body.index(node) - 1]
    except IndexError:
        return None

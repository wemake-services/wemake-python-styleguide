import ast


def count_boolops(node: ast.AST) -> int:
    """Counts how many ``BoolOp`` nodes there are in a node."""
    return len([
        subnode
        for subnode in ast.walk(node)
        if isinstance(subnode, ast.BoolOp)
    ])

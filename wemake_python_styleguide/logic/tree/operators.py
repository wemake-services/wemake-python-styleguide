import ast

from wemake_python_styleguide.logic.nodes import get_parent


def unwrap_unary_node(node: ast.AST) -> ast.AST:
    """
    Returns a real unwrapped node from the unary wrapper.

    It recursively unwraps any level of unary operators.
    Returns the node itself if it is not wrapped in unary operator.
    """
    while True:
        if not isinstance(node, ast.UnaryOp):
            return node
        node = node.operand


def get_parent_ignoring_unary(node: ast.AST) -> ast.AST | None:
    """
    Returns real parent ignoring proxy unary parent level.

    What can go wrong?

    1. Number can be negative: ``x = -1``,
       so ``1`` has ``UnaryOp`` as parent, but should return ``Assign``
    2. Some values can be negated: ``x = --some``,
       so ``some`` has ``UnaryOp`` as parent, but should return ``Assign``

    """
    while True:
        parent = get_parent(node)
        if parent is None or not isinstance(parent, ast.UnaryOp):
            return parent
        node = parent


def max_consecutive_unary_operators(
    node: ast.AST,
    operator: type[ast.unaryop],
) -> int:
    """Counts the maximum number of consecutive identical unary operators."""
    current_streak = 0
    max_streak = 0
    current = node

    while True:
        parent = get_parent(current)

        if not isinstance(parent, ast.UnaryOp):
            return max(current_streak, max_streak)

        if isinstance(parent.op, operator):
            current_streak += 1
        else:
            max_streak = max(max_streak, current_streak)
            current_streak = 0

        current = parent


def get_reduced_unary_operators(
    node: ast.AST,
    opchain: list[type[ast.unaryop]] | None = None,
) -> list[type[ast.unaryop]]:
    """Returns a sequence of significant unary operators."""
    if opchain is None:
        opchain = []

    parent = get_parent(node)
    if not isinstance(parent, ast.UnaryOp):
        return opchain

    if not isinstance(parent.op, ast.UAdd):
        lastop = opchain[-1] if opchain else None
        if lastop and isinstance(parent.op, lastop):
            opchain.pop()
        else:
            opchain.append(type(parent.op))

    return get_reduced_unary_operators(parent, opchain)

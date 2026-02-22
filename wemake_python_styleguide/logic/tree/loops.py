import ast

from wemake_python_styleguide.compat.aliases import ForNodes
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.types import AnyLoop, AnyNodes


def _does_loop_contain_node(
    loop: AnyLoop | None,
    to_check: ast.AST,
) -> bool:
    """
    Helper function to check for break statement in a nested loop.

    If a loop contains a loop with a break, this ensures that
    we don't count the outside loop as having a break.
    """
    if loop is None:
        return False

    return any(to_check is inner_node for inner_node in ast.walk(loop))


def is_in_try_except(node: ast.AST) -> bool:
    """Checks whether a node is directly inside a ``try/except`` block."""
    parent = get_parent(node)
    while parent is not None:
        if isinstance(parent, ast.Try) and parent.handlers:
            return True
        # Stop at function/class boundaries — don't look past them
        if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            break
        parent = get_parent(parent)
    return False


def has_break(
    node: AnyLoop,
    *,
    break_nodes: AnyNodes,
) -> bool:
    """Checks whether loop contains a break statement."""
    closest_loop = None

    for subnode in ast.walk(node):
        if isinstance(subnode, (*ForNodes, ast.While)) and subnode is not node:
            closest_loop = subnode

        if isinstance(subnode, break_nodes):
            is_nested_break = _does_loop_contain_node(
                closest_loop,
                subnode,
            )
            if not is_nested_break:
                return True
    return False


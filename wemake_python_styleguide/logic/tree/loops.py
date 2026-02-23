import ast

from wemake_python_styleguide.compat.aliases import ForNodes
from wemake_python_styleguide.logic.walk import tree as walk
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
    # Find the closest Try or scope-boundary parent, whichever comes first.
    closest = walk.get_closest_parent(
        node,
        (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Try),
    )
    return isinstance(closest, ast.Try) and bool(closest.handlers)


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

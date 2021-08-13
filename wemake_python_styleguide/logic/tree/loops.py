import ast
from typing import Iterable, List, Optional, Union

from wemake_python_styleguide.compat.aliases import ForNodes
from wemake_python_styleguide.types import AnyLoop, AnyNodes

_ForAndElseASTNode = Union[ast.For, List[ast.stmt]]


def _does_loop_contain_node(
    loop: Optional[AnyLoop],
    to_check: ast.AST,
) -> bool:
    """
    Helper function to check for break statement in a nested loop.

    If a loop contains a loop with a break, this ensures that
    we don't count the outside loop as having a break.
    """
    if loop is None:
        return False

    for inner_node in ast.walk(loop):
        # We are checking this specific node, not just any `break`:
        if to_check is inner_node:
            return True
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
                closest_loop, subnode,
            )
            if not is_nested_break:
                return True
    return False


def has_else(node: ast.For) -> bool:
    """Tells if this node or ``for`` chain ends with an ``else`` expression."""
    if not isinstance(node, ast.For):
        return False
    last_elem = tuple(chain(node))[-1]
    return bool(last_elem)


def chain(node: ast.For) -> Iterable[_ForAndElseASTNode]:
    """
    Yields the whole chain of ``for`` statements.

    This function also does go not up in the tree
    to find all parent ``for`` nodes. The rest order is preserved.
    The first one to return is the node itself.

    The last element of array is always a list of expressions that represent
    the last ``else`` node in the chain.
    That's ugly, but that's how ``ast`` works in python.
    """
    iterator: _ForAndElseASTNode = node
    yield iterator

    while True:
        if not isinstance(iterator, ast.For):
            return

        next_for = iterator.orelse
        if len(next_for) == 1 and isinstance(next_for[0], ast.For):
            yield next_for[0]
            iterator = next_for[0]
        else:
            yield next_for
            iterator = next_for

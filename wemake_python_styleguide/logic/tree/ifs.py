import ast
from collections.abc import Iterable
from typing import TypeAlias

_IfAndElifASTNode: TypeAlias = ast.If | list[ast.stmt]


def has_else(node: ast.If) -> bool:
    """Tells if this node or ``if`` chain ends with an ``else`` expression."""
    last_elem = tuple(chain(node))[-1]
    return bool(last_elem)


def chain(node: ast.If) -> Iterable[_IfAndElifASTNode]:
    """
    Yields the whole chain of ``if`` statements.

    This function also does go not up in the tree
    to find all parent ``if`` nodes. The rest order is preserved.
    The first one to return is the node itself.

    The last element of array is always a list of expressions that represent
    the last ``elif`` or ``else`` node in the chain.
    That's ugly, but that's how ``ast`` works in python.
    """
    iterator: _IfAndElifASTNode = node
    yield iterator

    while True:
        if not isinstance(iterator, ast.If):
            return

        next_if = iterator.orelse
        if len(next_if) == 1 and isinstance(next_if[0], ast.If):
            yield next_if[0]
            iterator = next_if[0]
        else:
            yield next_if
            iterator = next_if

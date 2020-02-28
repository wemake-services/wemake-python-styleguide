import ast
from typing import Iterable, List, Optional, Union

from wemake_python_styleguide.types import AnyNodes

_IfAndElifASTNode = Union[ast.If, List[ast.stmt]]


def has_elif(node: ast.If) -> bool:
    """Tells if this node is a part of a ``if`` chain or just a single one."""
    return getattr(node, 'wps_if_chain', False)  # noqa: WPS425


def has_else(node: ast.If) -> bool:
    """Tells if this node or ``if`` chain ends with an ``else`` expression."""
    last_elem = tuple(chain(node))[-1]
    return bool(last_elem)


def root_if(node: ast.If) -> Optional[ast.If]:
    """Returns the previous ``if`` node in the chain if it exists."""
    return getattr(node, 'wps_if_chained', None)


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


def has_nodes(
    to_check: AnyNodes,
    iterable: Iterable[ast.AST],
) -> bool:
    """Finds the given nodes types in ``if`` body."""
    return any(
        isinstance(line, to_check)
        for line in iterable
    )

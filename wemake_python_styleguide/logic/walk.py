import ast
from typing import Iterator, Optional, Type, TypeVar, Union

from typing_extensions import TypeAlias

from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.types import AnyNodes

_SubnodeType = TypeVar('_SubnodeType', bound=ast.AST)
_IsInstanceContainer: TypeAlias = Union[AnyNodes, type]


def is_contained(
    node: ast.AST,
    to_check: _IsInstanceContainer,
) -> bool:
    """
    Checks whether node does contain given subnode types.

    Goes down by the tree to check all children.
    """
    return any(isinstance(child, to_check) for child in ast.walk(node))


def get_closest_parent(
    node: ast.AST,
    parents: _IsInstanceContainer,
) -> Optional[ast.AST]:
    """Returns the closes parent of a node of requested types."""
    parent = get_parent(node)
    while True:
        if parent is None:
            return None
        if isinstance(parent, parents):
            return parent
        parent = get_parent(parent)


def is_contained_by(node: ast.AST, container: ast.AST) -> bool:
    """
    Tells you if a node is contained by a given container.

    Goes up by the tree of ``node`` to check all parents.
    Works with specific instances.
    """
    parent = get_parent(node)
    while True:
        if parent is None:
            return False
        if parent == container:
            return True
        parent = get_parent(parent)


def get_subnodes_by_type(
    node: ast.AST,
    subnodes_type: Type[_SubnodeType],
) -> Iterator[_SubnodeType]:
    """Returns the list of subnodes of given node with given subnode type."""
    for child in ast.walk(node):
        if isinstance(child, subnodes_type):
            yield child

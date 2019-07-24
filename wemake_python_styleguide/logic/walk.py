# -*- coding: utf-8 -*-

import ast
from typing import Iterator, Type, TypeVar, Union

from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.types import AnyNodes

_SubnodeType = TypeVar('_SubnodeType', bound=ast.AST)
_IsInstanceContainer = Union[AnyNodes, type]


def is_contained(
    node: ast.AST,
    to_check: _IsInstanceContainer,
) -> bool:
    """Checks whether node does contain given subnode types."""
    for child in ast.walk(node):
        if isinstance(child, to_check):
            return True
    return False


def is_child_of(node: ast.AST, parents: _IsInstanceContainer) -> bool:
    """Checks whether node is inside a given set of parents or not."""
    parent = get_parent(node)
    if parent is None:
        return False
    if isinstance(parent, parents):
        return True
    return is_child_of(parent, parents)


def get_subnodes_by_type(
    node: ast.AST,
    subnodes_type: Type[_SubnodeType],
) -> Iterator[_SubnodeType]:
    """Returns the list of subnodes of given node with given subnode type."""
    for child in ast.walk(node):
        if isinstance(child, subnodes_type):
            yield child

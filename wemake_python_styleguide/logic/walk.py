import ast
from collections.abc import Iterator
from typing import TypeAlias, TypeVar

from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.types import AnyNodes

_SubnodeType = TypeVar('_SubnodeType', bound=ast.AST)
_IsInstanceContainer: TypeAlias = AnyNodes | type


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
) -> ast.AST | None:
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
    subnodes_type: type[_SubnodeType],
) -> Iterator[_SubnodeType]:
    """Returns the list of subnodes of given node with given subnode type."""
    for child in ast.walk(node):
        if isinstance(child, subnodes_type):
            yield child


def extract_deleted_names(node: ast.AST) -> set[str]:
    """Extract all variable names deleted in the given AST node."""
    deleted: set[str] = set()

    for subnode in ast.walk(node):
        if isinstance(subnode, ast.Delete):
            for target in subnode.targets:
                if isinstance(target, ast.Name):
                    deleted.add(target.id)
    return deleted


def are_variables_deleted(
    variables: set[str],
    body: list[ast.stmt],
) -> bool:
    """Checks that given variables are deleted somewhere in the body."""
    deleted: set[str] = set()
    for stmt in body:
        deleted.update(extract_deleted_names(stmt))
    return variables.issubset(deleted)


def get_names_from_target(target: ast.expr) -> set[str]:
    """
    Extracts all variable names from a target expression.

    Works with simple names and unpacking, e.g.:
    - `for x in ...` -> {"x"}
    - `for x, y in ...` -> {"x", "y"}
    - `for (a, (b, c)) in ...` -> {"a", "b", "c"}
    """
    return {node.id for node in ast.walk(target) if isinstance(node, ast.Name)}

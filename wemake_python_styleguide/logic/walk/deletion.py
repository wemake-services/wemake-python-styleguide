import ast

from wemake_python_styleguide.logic.nodes import get_context
from wemake_python_styleguide.logic.walk.targets import (
    extract_names_from_targets,
)
from wemake_python_styleguide.types import ContextNodes


def extract_deleted_names(
    node: ast.AST, *, context: ContextNodes | None = None
) -> set[str]:
    """Extract all variable names deleted in the given AST node."""
    deleted: set[str] = set()

    for subnode in ast.walk(node):
        if not isinstance(subnode, ast.Delete):
            continue

        if context is not None and get_context(subnode) != context:
            continue

        deleted.update(extract_names_from_targets(subnode.targets))
    return deleted


def are_variables_deleted(
    variables: set[str],
    body: list[ast.stmt],
    *,
    context: ContextNodes | None = None,
) -> bool:
    """Checks that given variables are deleted somewhere in the body."""
    deleted: set[str] = set()
    for stmt in body:
        deleted.update(extract_deleted_names(stmt, context=context))
    return variables.issubset(deleted)

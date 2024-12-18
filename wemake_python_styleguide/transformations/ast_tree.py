import ast

from wemake_python_styleguide.transformations.ast.enhancements import (
    set_node_context,
)


def _set_parent(tree: ast.AST) -> ast.AST:
    """
    Sets parents for all nodes that do not have this prop.

    This step is required due to how `flake8` works.
    It does not set the same properties as `ast` module.

    This function was the cause of `issue-112`. Twice.
    Since the ``0.6.1`` we use ``'wps_parent'`` with a prefix.
    This should fix the issue with conflicting plugins.

    .. versionchanged:: 0.0.11
    .. versionchanged:: 0.6.1

    """
    for statement in ast.walk(tree):
        for child in ast.iter_child_nodes(statement):
            setattr(child, 'wps_parent', statement)  # noqa: B010
    return tree


def transform(tree: ast.AST) -> ast.AST:
    """
    Mutates the given ``ast`` tree.

    Applies all possible transformations.

    Ordering:
    - initial ones
    - bugfixes
    - enhancements

    """
    pipeline = (
        # Initial, should be the first ones, ordering inside is important:
        _set_parent,
        # Enhancements, order is not important:
        set_node_context,
    )

    for transformation in pipeline:
        tree = transformation(tree)
    return tree

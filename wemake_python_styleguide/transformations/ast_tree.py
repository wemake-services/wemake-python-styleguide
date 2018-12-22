# -*- coding: utf-8 -*-

import ast

from pep8ext_naming import NamingChecker

from wemake_python_styleguide.transformations.ast.bugfixes import (
    fix_async_offset,
    fix_line_number,
)
from wemake_python_styleguide.transformations.ast.enhancements import (
    set_if_chain,
)


class _ClassVisitor(ast.NodeVisitor):
    """Used to set method types inside classes."""

    def __init__(self, transformer: NamingChecker) -> None:
        super().__init__()
        self.transformer = transformer

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
        self.transformer.tag_class_functions(node)
        self.generic_visit(node)


def _set_parent(tree: ast.AST) -> ast.AST:
    """
    Sets parents for all nodes that do not have this prop.

    This step is required due to how `flake8` works.
    It does not set the same properties as `ast` module.

    This function was the cause of `issue-112`.

    .. versionchanged:: 0.0.11

    """
    for statement in ast.walk(tree):
        for child in ast.iter_child_nodes(statement):
            setattr(child, 'parent', statement)
    return tree


def _set_function_type(tree: ast.AST) -> ast.AST:
    """
    Sets the function type for methods.

    Can set: `method`, `classmethod`, `staticmethod`.

    .. versionchanged:: 0.3.0

    """
    transformer = _ClassVisitor(NamingChecker(tree, 'stdin'))
    transformer.visit(tree)
    return tree


def transform(tree: ast.AST) -> ast.AST:
    """
    Mutates the given ``ast`` tree.

    Applies all possible tranformations.

    Ordering:
    - initial ones
    - bugfixes
    - enhancements

    """
    pipeline = (
        # Initial, should be the first ones, ordering inside is important:
        _set_parent,
        _set_function_type,

        # Bugfixes, order is not important:
        fix_async_offset,
        fix_line_number,

        # Enhancements, order is not important:
        set_if_chain,
    )

    for tranformation in pipeline:
        tree = tranformation(tree)
    return tree

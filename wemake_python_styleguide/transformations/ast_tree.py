# -*- coding: utf-8 -*-

import ast

from pep8ext_naming import NamingChecker


class _ClassVisitor(ast.NodeVisitor):
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


def _fix_async_offset(tree: ast.AST) -> ast.AST:
    """
    Fixes ``col_offest`` values for async nodes.

    This is a temporary check for async-based expressions, because offset
    for them isn't calculated properly. We can calculate right version
    of offset with subscripting ``6`` (length of "async " part).

    Affected ``python`` versions:

    - all versions below ``python3.6.7``

    Read more:
        https://bugs.python.org/issue29205
        https://github.com/wemake-services/wemake-python-styleguide/issues/282

    """
    nodes_to_fix = (
        ast.AsyncFor,
        ast.AsyncWith,
        ast.AsyncFunctionDef,
    )
    for node in ast.walk(tree):
        if isinstance(node, nodes_to_fix):
            error = 6 if node.col_offset % 4 != 0 else 0
            node.col_offset = node.col_offset - error
    return tree


def transform(tree: ast.AST) -> ast.AST:
    """
    Mutates the given ``ast`` tree.

    Applies all possible tranformations.
    """
    pipeline = (
        _set_parent,
        _set_function_type,
        _fix_async_offset,
    )

    for tranformation in pipeline:
        tree = tranformation(tree)
    return tree

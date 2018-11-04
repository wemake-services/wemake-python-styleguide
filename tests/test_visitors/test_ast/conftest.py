# -*- coding: utf-8 -*-

import ast
from textwrap import dedent

import pytest
from pep8ext_naming import NamingChecker


class _ClassVisitor(ast.NodeVisitor):
    def __init__(self, transformer: NamingChecker) -> None:
        super().__init__()
        self.transformer = transformer

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
        self.transformer.tag_class_functions(node)
        self.generic_visit(node)


def _maybe_set_parent(tree: ast.AST) -> ast.AST:
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


def _maybe_set_function_type(tree: ast.AST) -> ast.AST:
    """
    Sets the function type for methods.

    Can set: `method`, `classmethod`, `staticmethod`.

    .. versionchanged:: 0.3.0

    """
    transformer = _ClassVisitor(NamingChecker(tree, 'stdin'))
    transformer.visit(tree)
    return tree


@pytest.fixture(scope='session')
def parse_ast_tree():
    """
    Helper function to convert code to ast.

    This helper mimics some transformations that generally
    happen in different `flake8` plugins that we rely on.

    This list can be extended only when there's a direct need to
    replicate the existing behavior from other plugin.

    It is better to import and reuse the required transformation.
    But in case it is impossible to do, you can reinvent it.

    Order is important.
    """
    transformation_pipeline = [
        _maybe_set_parent,
        _maybe_set_function_type,
    ]

    def factory(code: str, do_compile: bool = True) -> ast.AST:
        code_to_parse = dedent(code)

        if do_compile:
            # We need to compile to check some syntax features
            # that are validated after the `ast` is processed:
            # like double arguments or `break` outside of loops.
            compile(code_to_parse, '<filename>', 'exec')  # noqa: Z421
        tree = ast.parse(code_to_parse)

        for transform in transformation_pipeline:
            tree = transform(tree)
        return tree

    return factory

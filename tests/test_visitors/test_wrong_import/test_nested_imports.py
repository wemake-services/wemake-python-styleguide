# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_import import (
    NestedImportViolation,
    WrongImportVisitor,
)

nested_function_import = """
def function():
    import os
"""

nested_function_from_import = """
def function():
    from os import path
"""

nested_method_import = """
class Test:
    def with_import(self):
        import os
"""

nested_method_from_import = """
class Test:
    def with_import(self):
        from os import path
"""


@pytest.mark.parametrize('code', [
    nested_function_import,
    nested_function_from_import,
    nested_method_import,
    nested_method_from_import,
])
def test_nested_import(assert_errors, parse_ast_tree, code):
    """Testing that nested imports are restricted."""
    tree = parse_ast_tree(code)

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [NestedImportViolation])


def test_regular_import(assert_errors, parse_ast_tree):
    """Testing that regular imports are allowed."""
    tree = parse_ast_tree('import os')

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])


def test_regular_from_import(assert_errors, parse_ast_tree):
    """Testing that regular from imports are allowed."""
    tree = parse_ast_tree('from os import path')

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])

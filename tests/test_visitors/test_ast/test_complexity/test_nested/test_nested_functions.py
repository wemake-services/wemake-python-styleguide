# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.errors.best_practices import (
    NestedFunctionViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.nested import (
    NESTED_FUNCTIONS_WHITELIST,
    NestedComplexityVisitor,
)

nested_function = """
def container():
    def {0}(): ...
"""

nested_method = """
class Raw:
    def container(self):
        def {0}(): ...
"""


@pytest.mark.parametrize('code', [
    nested_function,
    nested_method,
])
def test_nested_function(assert_errors, parse_ast_tree, code, default_options):
    """Testing that nested functions are restricted."""
    tree = parse_ast_tree(code.format('nested'))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedFunctionViolation])


@pytest.mark.parametrize('whitelist_name', NESTED_FUNCTIONS_WHITELIST)
@pytest.mark.parametrize('code', [
    nested_function,
    nested_method,
])
def test_whitelist_nested_functions(
    assert_errors, parse_ast_tree, whitelist_name, code, default_options,
):
    """Testing that it is possible to nest whitelisted functions."""
    tree = parse_ast_tree(code.format(whitelist_name))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_lambda_nested_functions(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that it is possible to nest lambda inside functions."""
    tree = parse_ast_tree("""
    def container():
        lazy_value = lambda: 12
    """)

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_lambda_nested_lambdas(assert_errors, parse_ast_tree, default_options):
    """
    Testing that it is restricted to nest lambdas.

    See: https://github.com/wemake-services/wemake-python-styleguide/issues/94
    """
    tree = parse_ast_tree("""
    def container():
        nested_lambda = lambda: lambda value: value + 12
    """)

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedFunctionViolation])


def test_lambda_nested_method(assert_errors, parse_ast_tree, default_options):
    """Testing that it is possible to nest lambda inside methods."""
    tree = parse_ast_tree("""
    class Raw:
        def container(self):
            lazy_value = lambda: 12
    """)

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

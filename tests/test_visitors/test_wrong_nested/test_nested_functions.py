# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_nested import (
    NESTED_FUNCTIONS_WHITELIST,
    NestedFunctionViolation,
    WrongNestedVisitor,
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
def test_nested_function(assert_errors, parse_ast_tree, code):
    """Testing that nested functions are restricted."""
    tree = parse_ast_tree(code.format('nested'))

    visiter = WrongNestedVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [NestedFunctionViolation])


@pytest.mark.parametrize('whitelist_name', NESTED_FUNCTIONS_WHITELIST)
@pytest.mark.parametrize('code', [
    nested_function,
    nested_method,
])
def test_whitelist_nested_functions(
    assert_errors, parse_ast_tree, whitelist_name, code,
):
    """Testing that it is possible to nest whitelisted functions."""
    tree = parse_ast_tree(code.format(whitelist_name))

    visiter = WrongNestedVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])


def test_lambda_nested_functions(assert_errors, parse_ast_tree):
    """Testing that it is possible to nest lambda inside functions."""
    tree = parse_ast_tree("""
    def container():
        lazy_value = lambda: 12
    """)

    visiter = WrongNestedVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])


def test_lambda_nested_lambdas(assert_errors, parse_ast_tree):
    """Testing that it is possible to nest lambdas."""
    tree = parse_ast_tree("""
    def container():
        nested_lambda = lambda: lambda value: value + 12
    """)

    visiter = WrongNestedVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])


def test_lambda_nested_method(assert_errors, parse_ast_tree):
    """Testing that it is possible to nest lambda inside methods."""
    tree = parse_ast_tree("""
    class Raw:
        def container(self):
            lazy_value = lambda: 12
    """)

    visiter = WrongNestedVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])

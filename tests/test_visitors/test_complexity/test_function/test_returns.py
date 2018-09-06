# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.complexity.function import (
    FunctionComplexityVisitor,
    TooManyReturnsViolation,
)

function_without_returns = """
def function(): ...
"""

function_with_returns = """
def function():
    if 1 > 2:
        return 1
    return 0
"""


@pytest.mark.parametrize('code', [
    function_without_returns,
    function_with_returns,
])
def test_returns_correct_count(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that returns counted correctly."""
    tree = parse_ast_tree(code)

    visiter = FunctionComplexityVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])


@pytest.mark.parametrize('code', [
    function_with_returns,
])
def test_returns_wrong_count(assert_errors, parse_ast_tree, options, code):
    """Testing that many returns raises a warning."""
    tree = parse_ast_tree(code)

    option_values = options(max_returns=1)
    visiter = FunctionComplexityVisitor(option_values)
    visiter.visit(tree)

    assert_errors(visiter, [TooManyReturnsViolation])

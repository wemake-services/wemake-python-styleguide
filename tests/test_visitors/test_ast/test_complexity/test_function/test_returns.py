# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
    TooManyReturnsViolation,
)

function_without_returns = 'def function(): ...'

function_with_returns = """
{0} def function():
    if 1 > 2:
        return 1
    return 0
"""


@pytest.mark.parametrize('code', [
    function_without_returns,
    function_with_returns,
])
@pytest.mark.parametrize('mode', [
    'async',  # coroutine
    '',  # regular function
])
def test_returns_correct_count(
    assert_errors, parse_ast_tree, code, default_options, mode,
):
    """Testing that returns counted correctly."""
    tree = parse_ast_tree(code.format(mode))

    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_with_returns,
])
@pytest.mark.parametrize('mode', [
    'async',  # coroutine
    '',  # regular function
])
def test_returns_wrong_count(
    assert_errors, parse_ast_tree, options, code, mode,
):
    """Testing that many returns raises a warning."""
    tree = parse_ast_tree(code.format(mode))

    option_values = options(max_returns=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyReturnsViolation])

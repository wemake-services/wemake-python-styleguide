# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.complexity.function import (
    FunctionComplexityVisitor,
    TooManyExpressionsViolation,
)

function_without_expressions = """
def function(): ...
"""

function_with_expressions = """
def function():
    print(12)
    print(12 / 1)
"""


@pytest.mark.parametrize('code', [
    function_without_expressions,
    function_with_expressions,
])
def test_expressions_correct_count(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that expressions counted correctly."""
    tree = parse_ast_tree(code)

    visiter = FunctionComplexityVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])


@pytest.mark.parametrize('code', [
    function_with_expressions,
])
def test_expressions_wrong_count(assert_errors, parse_ast_tree, options, code):
    """Testing that many expressions raises a warning."""
    tree = parse_ast_tree(code)

    option_values = options(max_expressions=1)
    visiter = FunctionComplexityVisitor(option_values)
    visiter.visit(tree)

    assert_errors(visiter, [TooManyExpressionsViolation])

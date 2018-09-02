# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.complexity.function import (
    FunctionComplexityVisitor,
    TooManyLocalsViolation,
)

function_with_locals = """
def function():
    local_variable1 = 1
    local_variable2 = 2
    _ = None  # `_` is not counted
"""

function_with_locals_redefinition = """
def function():
    local_variable1 = 1
    local_variable2 = 2

    local_variable1 += 3
    local_variable2 = local_variable1 + 4
"""

function_with_locals_and_params = """
def function(param):
    local_variable1 = 1
    param = param + 2
    param += 3
"""


@pytest.mark.parametrize('code', [
    function_with_locals,
    function_with_locals_redefinition,
    function_with_locals_and_params,
])
def test_locals_correct_count(assert_errors, parse_ast_tree, options, code):
    """
    Testing that local variables are counted correctly.

    Regression test for #74.
    See: https://github.com/wemake-services/wemake-python-styleguide/issues/74
    """
    option_values = options(max_local_variables=2)
    tree = parse_ast_tree(code)

    visiter = FunctionComplexityVisitor()
    visiter.provide_options(option_values)
    visiter.visit(tree)

    assert_errors(visiter, [])


@pytest.mark.parametrize('code', [
    function_with_locals,
    function_with_locals_redefinition,
    function_with_locals_and_params,
])
def test_locals_wrong_count(assert_errors, parse_ast_tree, options, code):
    """
    Testing that local variables are counted correctly.

    Regression test for #74.
    See: https://github.com/wemake-services/wemake-python-styleguide/issues/74
    """
    option_values = options(max_local_variables=1)
    tree = parse_ast_tree(code)

    visiter = FunctionComplexityVisitor()
    visiter.provide_options(option_values)
    visiter.visit(tree)

    assert_errors(visiter, [TooManyLocalsViolation])

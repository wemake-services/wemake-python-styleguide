# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
    TooManyLocalsViolation,
)

function_with_locals = """
{0}def function():
    local_variable1 = 1
    local_variable2 = 2
    _ = None  # `_` is not counted
"""

function_with_locals_redefinition = """
{0}def function():
    local_variable1 = 1
    local_variable2 = 2

    local_variable1 += 3
    local_variable2 = local_variable1 + 4
"""

function_with_locals_and_params = """
{0}def function(param):
    local_variable1 = 1
    param = param + 2
    param += 3
"""

function_with_comprehension = """
{0}def function():
    variable1 = [node for node in parse()]
    variable2 = [xml for xml in variable1]
"""


@pytest.mark.parametrize('code', [
    function_with_locals,
    function_with_locals_redefinition,
    function_with_locals_and_params,
    function_with_comprehension,
])
@pytest.mark.parametrize('mode', [
    'async ',  # coroutine
    '',  # regular function
])
def test_locals_correct_count(
    assert_errors,
    parse_ast_tree,
    options,
    code,
    mode,
):
    """
    Testing that local variables are counted correctly.

    Regression test for #74.
    See: https://github.com/wemake-services/wemake-python-styleguide/issues/74

    Regression test for #247
    See: https://github.com/wemake-services/wemake-python-styleguide/issues/247
    """
    option_values = options(max_local_variables=2)
    tree = parse_ast_tree(code.format(mode))

    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_with_locals,
    function_with_locals_redefinition,
    function_with_locals_and_params,
    function_with_comprehension,
])
@pytest.mark.parametrize('mode', [
    'async ',  # coroutine
    '',  # regular function
])
def test_locals_wrong_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    options,
    code,
    mode,
):
    """
    Testing that local variables are counted correctly.

    Regression test for #74.
    See: https://github.com/wemake-services/wemake-python-styleguide/issues/74

    Regression test for #247
    See: https://github.com/wemake-services/wemake-python-styleguide/issues/247
    """
    option_values = options(max_local_variables=1)
    tree = parse_ast_tree(code.format(mode))

    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyLocalsViolation])
    assert_error_text(visitor, '2')

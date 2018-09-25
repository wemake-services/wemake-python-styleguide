# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
    TooManyElifsViolation,
)

function_with_elifs = """
def test_module():
    if 1 > 2:
        print(1)
    elif 2 > 3:
        print(2)
    elif 3 > 4:
        print(3)
    else:
        print(4)
"""

function_with_ifs = """
def test_module():
    if True:
        print(1)
    if 2 > 3:
        print(2)
    if 3 > 4:
        print(3)
"""

function_with_raw_if = """
def function():
    if 1 == 2:
        print(1)
"""

function_with_if_else = """
def function(param):
    if param == 2:
        print(1)
    else:
        print(2)
"""

function_with_ternary = """
def with_ternary(some_value):
    return [some_value] if some_value > 1 else []
"""


@pytest.mark.parametrize('code', [
    function_with_elifs,
    function_with_ifs,
    function_with_raw_if,
    function_with_if_else,
    function_with_ternary,
])
def test_elif_correct_count(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that all `if`/`elif`/`else` stuff is allowed."""
    tree = parse_ast_tree(code)

    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_with_elifs,
])
def test_elif_incorrect_count(assert_errors, parse_ast_tree, code, options):
    """Testing that incorrect number of `elif` stuff is restricted."""
    tree = parse_ast_tree(code)

    option_values = options(max_elifs=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyElifsViolation])

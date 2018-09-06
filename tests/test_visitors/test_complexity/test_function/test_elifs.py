# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.complexity.function import (
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

function_with_raw_if = """
def function():
    if 1 == 2:
        print(1)
"""

function_with_if_else = """
def function(param):
    if 1 == 2:
        print(1)
    else:
        print(2)
"""


@pytest.mark.parametrize('code', [
    function_with_elifs,
    function_with_raw_if,
    function_with_if_else,
])
def test_elif_correct_count(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that all `if`/`elif`/`else` stuff is allowed."""
    tree = parse_ast_tree(code)

    visiter = FunctionComplexityVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])


def test_elif_incorrect_count(assert_errors, parse_ast_tree, options):
    """Testing that incorrect number of `elif` stuff is restricted."""
    tree = parse_ast_tree(function_with_elifs)

    option_values = options(max_elifs=1)
    visiter = FunctionComplexityVisitor(option_values)
    visiter.visit(tree)

    assert_errors(visiter, [TooManyElifsViolation])

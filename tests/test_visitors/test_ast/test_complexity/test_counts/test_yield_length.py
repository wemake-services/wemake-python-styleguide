# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.counts import (
    TooLongYieldTupleViolation,
    YieldTupleVisitor,
)

single_yield = """
def function_name():
    i = 0
    while True:
        yield i
        i = i + 1
"""

short_yield = """
def function_name():
    i = 0
    while True:
        yield i + 1, i + 2, i + 3
"""

long_yield = """
def function_name(foo, bar, baz):
    i = 0
    while True:
        yield i + 1, i + 2, i + 3, foo + 1, bar + 1, baz + 1
"""


@pytest.mark.parametrize('code', [
    single_yield,
    short_yield,
])
def test_module_counts_normal(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that classes and functions in a module work well."""
    tree = parse_ast_tree(code)

    visitor = YieldTupleVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    long_yield,
])
def test_module_counts_violation(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    visitor = YieldTupleVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongYieldTupleViolation])
    assert_error_text(visitor, 6)

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.complexity import (
    TooLongCompareViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    ConditionsVisitor,
)

# Correct:

empty_module = ''
one_compare = 'x > 1'
two_compare = 'x < y() >= 2'

one_equals = 'x == 1'
two_equals = 'x == call() == prop.attr'
only_equals = 'x == y == z == c'

one_non_equals = 'x != 1'
two_non_equals = 'x != call() != prop.attr'
only_non_equals = 'x != y != z != c'

mixed_short_equals = 'x != y == z'

# Wrong:

three_similar_compare = 'x > y > z > c'
three_close_compare = 'x < y > z >= c'
three_compare = 'x == attr.prop != method <= 1'
mixed_long_equals = 'x != y == z != c'


@pytest.mark.parametrize('code', [
    empty_module,
    one_compare,
    two_compare,
    one_equals,
    two_equals,
    only_equals,
    one_non_equals,
    two_non_equals,
    only_non_equals,
    mixed_short_equals,
])
def test_module_compare_counts_normal(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that compare in a module work well."""
    tree = parse_ast_tree(code)

    visitor = ConditionsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    three_similar_compare,
    three_compare,
    three_close_compare,
    mixed_long_equals,
])
def test_module_compare_counts_violation(
    monkeypatch,
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    visitor = ConditionsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongCompareViolation])

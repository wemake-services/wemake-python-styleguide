# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    ImplicitTernaryViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    BooleanConditionVisitor,
)

# Correct:

not_ternary1 = 'cond() and {0} and {1}'
not_ternary2 = 'cond() or {0} and {1}'
not_ternary3 = 'cond() or {0} or {1}'
not_ternary4 = 'cond() and extra and {0} or {1}'
not_ternary5 = 'cond() or extra and {0} or {1}'
not_ternary6 = '{0} and {1}'
not_ternary7 = '{0} or {1}'
not_ternary8 = 'cond() > {0} or {1}'
not_ternary9 = 'cond() and {0} or {1} or extra'

ternary = '{0} if cond() else {1}'

# Wrong:

possible_ternary = 'cond() and {0} or {1}'


@pytest.mark.parametrize('code', [
    possible_ternary,
])
@pytest.mark.parametrize('first, second', [
    ('one.attr', 'two'),
    ('None', 'value()'),
    ('value.method()', 'None'),
    ('True', 'False'),
    ('False', 'True'),
])
def test_implicit_ternary(
    code,
    first,
    second,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing implicit ternary."""
    tree = parse_ast_tree(code.format(first, second))

    visitor = BooleanConditionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImplicitTernaryViolation])


@pytest.mark.parametrize('code', [
    not_ternary1,
    not_ternary2,
    not_ternary3,
    not_ternary4,
    not_ternary5,
    not_ternary6,
    not_ternary7,
    not_ternary8,
    not_ternary9,
    ternary,
])
@pytest.mark.parametrize('first, second', [
    ('one.attr', 'two'),
    ('None', 'value()'),
    ('value.method()', 'None'),
    ('True', 'False'),
    ('False', 'True'),
])
def test_regular_compare_not_ternary(
    code,
    first,
    second,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing regular compares and not ternaries."""
    tree = parse_ast_tree(code.format(first, second))

    visitor = BooleanConditionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
)
from wemake_python_styleguide.visitors.ast.comparisons import WrongOrderVisitor

if_with_is = 'if {0} is {1}: ...'
if_with_is_not = 'if {0} is not {1}: ...'

if_with_eq = 'if {0} == {1}: ...'
if_with_not_eq = 'if {0} != {1}: ...'
if_with_gt = 'if {0} > {1}: ...'
if_with_lt = 'if {0} < {1}: ...'
if_with_gte = 'if {0} >= {1}: ...'
if_with_lte = 'if {0} <= {1}: ...'

if_with_chained_comparisons1 = 'if 0 < {0} < {1}: ...'
if_with_chained_comparisons2 = 'if {0} > {1} > 0: ...'
if_with_chained_comparisons3 = 'if -1 > {0} > {1} > 0: ...'

if_with_in = 'if {0} in {1}: ...'
if_with_not_in = 'if {0} not in {1}: ...'

ternary = 'ternary = 0 if {0} > {1} else 1'
while_construct = 'while {0} > {1}: ...'
assert_construct = 'assert {0} == {1}'
assert_with_message = 'assert {0} == {1}, "message"'


@pytest.mark.parametrize('code', [
    if_with_is,
    if_with_is_not,

    if_with_eq,
    if_with_not_eq,
    if_with_lt,
    if_with_gt,
    if_with_lte,
    if_with_gte,

    if_with_chained_comparisons1,
    if_with_chained_comparisons2,
    if_with_chained_comparisons3,

    ternary,
    while_construct,
    assert_construct,
    assert_with_message,
])
@pytest.mark.parametrize('comparators', [
    ('first_name', 'second_name'),
    ('first_name', 'second_name + 1'),
    ('first_name', '"string constant"'),
    ('first_name', [1, 2, 3]),
    ('first_name', 'len(second_name)'),
    ('len(first_name)', 1),
    ('first_name.call()', 1),
    ('first_name.attr', 1),
    ('first_name + 10', 1),
    ('first_name + second_name', 1),
    ('error.code', 'errors[index].code'),
    (1, 2),
])
def test_comparison_variables(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Comparisons work well for left variables."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    if_with_in,
    if_with_not_in,
])
@pytest.mark.parametrize('comparators', [
    ('"string constant"', 'container'),
    (1, 'second_name'),
])
def test_comparison_variables_in_special_case(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Ensures that special case for `in` and `not in` is handled."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    if_with_is,
    if_with_is_not,

    if_with_eq,
    if_with_not_eq,
    if_with_lt,
    if_with_gt,
    if_with_lte,
    if_with_gte,

    ternary,
    while_construct,
    assert_construct,
    assert_with_message,
])
@pytest.mark.parametrize('comparators', [
    ('"string constant"', 'first_name'),
    ([1, 2, 3], 'first_name'),
    (1, 'len(first_name)'),
    (1, 'first_name.attr'),
    (1, 'first_name.call()'),
    (1, 'first_name + 10'),
    (1, 'first_name + second_name'),
])
def test_comparison_wrong_order(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Comparisons raise for left constants."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComparisonOrderViolation])


@pytest.mark.parametrize('comparators', [
    ('"string constant"', 'first_name'),
    ([1, 2, 3], 'first_name'),
    (1, 'len(first_name)'),
    (1, 'first_name.call()'),
    (1, 'first_name + 10'),
    (1, 'first_name + second_name'),
])
def test_comparison_wrong_order_multiple(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """Comparisons raise multiple issues for left constants."""
    tree = parse_ast_tree(
        'if {0} > {1} and {0} < {1}: ...'.format(*comparators),
    )

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        ComparisonOrderViolation,
        ComparisonOrderViolation,
    ])

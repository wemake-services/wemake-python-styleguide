# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    ConstantComparisonViolation,
)
from wemake_python_styleguide.visitors.ast.comparisons import (
    ConstantComparisonVisitor,
)

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

    ternary,
    while_construct,
    assert_construct,
    assert_with_message,
])
@pytest.mark.parametrize('comparators', [
    ('first_name', 'second_name'),
    ('first_name', 1),
    (1, 'first_name'),
])
def test_non_literal(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that comparisons work well."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = ConstantComparisonVisitor(default_options, tree=tree)
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
    (1, 2),
    ('"string1"', '"string2"'),
    ('[1, 2, 3]', '(1, 2, 3)'),
    ('{"key": 1}', '{"a", "b"}'),
])
def test_literal(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that violations are when using literal comparisons."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = ConstantComparisonVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConstantComparisonViolation])


@pytest.mark.parametrize('code', [
    if_with_chained_comparisons1,
    if_with_chained_comparisons3,
])
@pytest.mark.parametrize('comparators', [
    (1, 'first_name'),
    (1, 1),
])
def test_literal_special1(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that special cases do work and raise warnings."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = ConstantComparisonVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConstantComparisonViolation])


@pytest.mark.parametrize('code', [
    if_with_chained_comparisons2,
    if_with_chained_comparisons3,
])
@pytest.mark.parametrize('comparators', [
    ('first_name', 1),
    (1, 1),
])
def test_literal_special2(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that special cases do work and raise warnings."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = ConstantComparisonVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConstantComparisonViolation])


@pytest.mark.parametrize('code', [
    if_with_chained_comparisons1,
    if_with_chained_comparisons2,
    if_with_chained_comparisons3,
])
def test_literal_special_without_errors(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that special cases do work and do not raise warnings."""
    tree = parse_ast_tree(code.format('first_name', 'second_name'))

    visitor = ConstantComparisonVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    ConstantComparisonViolation,
)
from wemake_python_styleguide.visitors.ast.comparisons import (
    RedundantComparisonVisitor,
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
assert_construct = 'assert {0} == {1}, "message"'


class Foo(object):
    """Return the pathname of the KOS root directory."""

    kind = 'Bar'


variable = Foo()
another_variable = Foo()


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
])
@pytest.mark.parametrize('comparators', [
    ('variable', '"test"'),
    ('variable', 'another_variable'),
    ('variable', '222'),
])
def test_not_redundant(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that comparisons work well."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = RedundantComparisonVisitor(default_options, tree=tree)
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
])
@pytest.mark.parametrize('comparators', [
    ('variable', 'variable'),
    ('another_variable', 'another_variable'),
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

    visitor = RedundantComparisonVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConstantComparisonViolation])


# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    MultipleInComparisonViolation,
)
from wemake_python_styleguide.visitors.ast.comparisons import MultipleInVisitor

if_with_multiple_in_comaprisons = 'if {0} in {1} in {2}: ...'
if_without_multiple_in_comparisons = 'if {0} in {1} : ...'

ternary = 'ternary = 0 if {0} in {1} else 1'
ternary_with_multiple_in = 'ternary = 0 if {0} in {1} in {2} else 1'
while_construct = 'while {0} in {1}: ...'
while_with_multiple_in = 'while {0} in {1} in {2}: ...'
if_with_refactored_in = 'if x_coord in line and line in square: ...'


@pytest.mark.parametrize('code', [
    if_without_multiple_in_comparisons,
    ternary,
    while_construct,
    if_with_refactored_in,
])
@pytest.mark.parametrize('comparators', [
    ('x', '6'),
    ('status', [True]),
    ('letter', ['a', 'b']),
])
def test_comparison_with_in(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Comparisons work well for single `in`."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = MultipleInVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    if_with_multiple_in_comaprisons,
    ternary_with_multiple_in,
    while_with_multiple_in,
])
@pytest.mark.parametrize('comparators', [
    ('line', 'sqaure', 'shape'),
    ('output', 'status', [True]),
    ('letter', 'line', 'book'),
])
def test_comparison_with_multiple_in(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Comparisons raise for multiple `in`s."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = MultipleInVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MultipleInComparisonViolation])

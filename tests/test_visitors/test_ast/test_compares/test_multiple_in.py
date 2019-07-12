# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    HeterogenousCompareViolation,
)
from wemake_python_styleguide.violations.consistency import (
    MultipleInCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import CompareSanityVisitor

if_with_multiple_in_compares = 'if {0} in {1} in {2}: ...'
if_without_multiple_in_compares = 'if {0} in {1}: ...'

ternary = 'ternary = 0 if {0} in {1} else 1'
ternary_with_multiple_in = 'ternary = 0 if {0} in {1} in {2} else 1'

while_construct = 'while {0} in {1}: ...'
while_with_multiple_in = 'while {0} in {1} in {2}: ...'


@pytest.mark.parametrize('code', [
    if_without_multiple_in_compares,
    ternary,
    while_construct,
])
@pytest.mark.parametrize('comparators', [
    ('x_coord', '6'),
    ('status', [True]),
    ('letter', ['a', 'b']),
])
def test_compare_with_in(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
    in_not_in,
):
    """Compares work well for single ``in``."""
    tree = parse_ast_tree(in_not_in(code.format(*comparators)))

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    if_with_multiple_in_compares,
    ternary_with_multiple_in,
    while_with_multiple_in,
])
@pytest.mark.parametrize('comparators', [
    ('line', 'sqaure', 'shape'),
    ('output', 'status', [True]),
    ('letter', 'line', 'book'),
])
def test_compare_with_multiple_in(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
    in_not_in,
):
    """Compares raise for multiple ``in`` cases."""
    tree = parse_ast_tree(in_not_in(code.format(*comparators)))

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MultipleInCompareViolation])


def test_compare_with_mixed_in(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Compares raise for multiple ``in`` and ``not in`` cases."""
    tree = parse_ast_tree('x in a not in b')

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        MultipleInCompareViolation,
        HeterogenousCompareViolation,
    ])

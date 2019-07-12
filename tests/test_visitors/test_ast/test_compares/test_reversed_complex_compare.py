# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    ReversedComplexCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import CompareSanityVisitor


@pytest.mark.parametrize('code', [
    'x > y >= z',
    'x > y > z',
])
def test_reversed_complex_compare(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that reversed compares raise a violation."""
    tree = parse_ast_tree(code)

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ReversedComplexCompareViolation])


@pytest.mark.parametrize('code', [
    'x < y <= z',
    'x < y < z',
    'x <= y < z',
    'x <= y <= z',
    'x == y == z',
    'x != y != z',
])
def test_correct_compare(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that compares work well."""
    tree = parse_ast_tree(code)

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

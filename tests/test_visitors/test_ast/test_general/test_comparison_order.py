# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
)
from wemake_python_styleguide.visitors.ast.order import WrongOrderVisitor

@pytest.mark.parametrize('code', [
    'a < 3',
    '0 < x < 1',
    'x == 3',
])

def test_comparison_normal(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that consistent comparisons (argument comes first) work well."""
    tree = parse_ast_tree(code)

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    '3 < x',
    '3 == x',
])

def test_wrong_comparison(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that violations are raised when inconsistent comparisons are used."""
    tree = parse_ast_tree(code)

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComparisonOrderViolation])
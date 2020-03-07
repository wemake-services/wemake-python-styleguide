import pytest

from wemake_python_styleguide.violations.best_practices import (
    HeterogenousCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import CompareSanityVisitor


@pytest.mark.parametrize('code', [
    'x > y < z',
    'x >= y < z',
    'x > y <= z',
    'x >= y <= z',
    'x < y > z',
    'x <= y > z',
    'x < y >= z',
    'x <= y >= z',
    'x > y != 0',
    'x < y == 0',
    'x >= y != 0',
    'x <= y == 0',
    'x == y != z',
    'long == x == y >= z',
    'call() != attr.prop in array',
    'item not in array == value',
])
def test_heterogenous_compare(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that compares with diffrent operators raise."""
    tree = parse_ast_tree(code)

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [HeterogenousCompareViolation])


@pytest.mark.parametrize('code', [
    'x == y == z',
    'z != y != x',
    'call() == other.prop',
    'x in y',
    'x not in y',
])
def test_correct_compare_operators(
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

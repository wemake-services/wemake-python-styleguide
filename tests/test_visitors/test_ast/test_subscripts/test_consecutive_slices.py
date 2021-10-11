import pytest

from wemake_python_styleguide.violations.best_practices import (
    ConsecutiveSlicesViolation,
)
from wemake_python_styleguide.visitors.ast.subscripts import SubscriptVisitor

usage_template = 'constant[{0}]'


@pytest.mark.parametrize('expression', [
    'a[1:][:3]',
    'a[1:3][3:]',
    'a[:][:]',
    'a[1:3][3:][2:]',
    'a[:c[d]][:5]["hello"]',
])
def test_forbidden_consecutive_slices(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that consecutive slices are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SubscriptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConsecutiveSlicesViolation])


@pytest.mark.parametrize('expression', [
    'a[:][:a[3:][4:]]',
    'a[:][:1]["hello"][:42][2:]',
])
def test_forbidden_multiple_consecutive_slices(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that consecutive slices are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SubscriptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        ConsecutiveSlicesViolation,
        ConsecutiveSlicesViolation,
    ])


@pytest.mark.parametrize('expression', [
    'a',
    'a[3:7]',
    'a[4][:5]',
    'a["hello"][4:]',
    'a[1:]["tram"][17:]',
    'a[a[:1]][a[1:2]][a[2:3]]',
    'a[1][2][3]',
])
def test_nonconsecutive_slices(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that non-consecutive slices are allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SubscriptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

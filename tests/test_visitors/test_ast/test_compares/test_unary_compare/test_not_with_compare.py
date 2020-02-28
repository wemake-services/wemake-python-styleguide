import pytest

from wemake_python_styleguide.violations.refactoring import (
    NotOperatorWithCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import UnaryCompareVisitor


@pytest.mark.parametrize('code', [
    'not x > 5',
    'not (x > 5)',
    'not some() > call.other()',
    'not some() <= call.other',
    'not first == second == third',
    'not (first == second) == third',
    'not ((first == second) == third)',
    'not first == (second == third)',
    'not (first == (second == third))',
    'not (first == second == third)',
    'not x != y',
    'not (x != y)',
    'not x in []',
    'not x not in x',
    'not (x not in x)',
    'not x is a',
    'not (x is a)',
])
def test_incorrect_unary_not_operator(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that compares with `not` raise a violation."""
    tree = parse_ast_tree(code)

    visitor = UnaryCompareVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NotOperatorWithCompareViolation])


@pytest.mark.parametrize('code', [
    'not some',
    'some is not None',
    'some not in other',
    'not call()',
    'x > 1',
    '(not call()) is False',
    '(not x) is a',
])
def test_correct_unary_operator(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that compares work well."""
    tree = parse_ast_tree(code)

    visitor = UnaryCompareVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

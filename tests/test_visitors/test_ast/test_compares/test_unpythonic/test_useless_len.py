import pytest

from wemake_python_styleguide.violations.refactoring import (
    UselessLenCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import CompareSanityVisitor


@pytest.mark.parametrize('code', [
    'len(some) > 0',
    'len(some) >= 0',
    'len(some) != 0',
    'len(some) <= 0',
    'len(some) < 0',
    'len(some) < -0',
    'len(some) < +0',
    'len(some) == 0',
    'len(some) == +0',
    'len(some) == -0',
    'len(some) >= 1',
    'len(some) >= +1',
    'len(some()) < 1',
    'len(-some()) < 1',
    '0 < len(some) < 1',
    'call() < 1 <= len(some)',
    '(x := len(some)) > 0',
])
def test_useless_len_call(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that compares with len raise a violation."""
    tree = parse_ast_tree(code)

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessLenCompareViolation])


@pytest.mark.parametrize('code', [
    'sum(some) == 0',
    'min(some) > 0',
    'len(some) > some_value',
    'len(some) < some_value.attr',
    'len(some) != some_value.method()',
    'len(some) != len(other)',
    'len(some) > 1',
    'len(some) <= 1',
    'len(some) == 1',
    'len(some) != 1',
    'len(some) > 5',
    'len(some) < 4',
    'len(some) == 10',
    'len(some) != 6',
    'ye >= len(str(emax))',
    '8 < len(call())',
    'len(str(abs(yc*xe))) <= -ye',
])
def test_correct_len_call(
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

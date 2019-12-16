# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    SameElementsInConditionViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    BooleanConditionVisitor,
)


@pytest.mark.parametrize('code', [
    'some or other',
    'other and some',
    'first or second and third',
    '(first or second) and third',
    'first or (second and third)',
    'very and complex and long and condition',
])
def test_regular_conditions(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correct conditions work."""
    tree = parse_ast_tree(code)

    visitor = BooleanConditionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'call() or call()',
    'attr.name and attr.name',
    '4 and 4',

    'name or name',
    'name and name',

    'name and (proxy or name)',

    'name and proxy and name',
    '(name and proxy) and name',
    'name and (proxy and name)',

    'name and name and name',
    'name or name or name',

    # Regression tests, see:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/1004
    'name or not name',
    'not name or name',
    'not name or not name',
    '+name and -name',
    '~name and name',
    'name and -name and not not name',
])
def test_duplicate_element(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that duplicates raise a violation."""
    tree = parse_ast_tree(code)

    visitor = BooleanConditionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [SameElementsInConditionViolation])


@pytest.mark.parametrize('code', [
    'name and proxy or name',
    '(name and proxy) or name',
])
def test_duplicate_element_and_ternary(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that duplicates raise two violations."""
    tree = parse_ast_tree(code)

    visitor = BooleanConditionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [SameElementsInConditionViolation])

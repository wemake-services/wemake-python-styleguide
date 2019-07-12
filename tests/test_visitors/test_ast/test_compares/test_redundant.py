# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    UselessCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import CompareSanityVisitor

create_variables = """
variable = 1
another_variable = 2
{0}
"""


@pytest.mark.parametrize('comparators', [
    ('variable', '"test"'),
    ('variable', 'variable.call()'),
    ('variable', 'variable.attr'),
    ('variable', 'len(variable)'),
    ('variable', 'another_variable'),
    ('variable', '222'),
])
def test_not_useless(
    assert_errors,
    parse_ast_tree,
    simple_conditions,
    comparators,
    default_options,
):
    """Testing that compares work well."""
    tree = parse_ast_tree(
        create_variables.format(simple_conditions.format(*comparators)),
    )

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', [
    ('variable', 'variable'),
    ('another_variable', 'another_variable'),
])
def test_useless(
    assert_errors,
    parse_ast_tree,
    simple_conditions,  # TODO: join with `test_useless_with_in`
    comparators,
    default_options,
):
    """Testing that violations are when comparing identical variable."""
    tree = parse_ast_tree(
        create_variables.format(simple_conditions.format(*comparators)),
    )

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessCompareViolation])


@pytest.mark.parametrize('comparators', [
    ('variable', 'variable'),
    ('another_variable', 'another_variable'),
])
def test_useless_with_in(  # TODO: join with `test_useless`
    assert_errors,
    parse_ast_tree,
    in_conditions,
    comparators,
    default_options,
):
    """Testing that violations are when comparing identical variable."""
    tree = parse_ast_tree(
        create_variables.format(in_conditions.format(*comparators)),
    )

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessCompareViolation])


def test_multiple_compare(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Ensuring than multiple useless compare returns a single violation."""
    tree = parse_ast_tree('assert some == some == some')

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessCompareViolation])

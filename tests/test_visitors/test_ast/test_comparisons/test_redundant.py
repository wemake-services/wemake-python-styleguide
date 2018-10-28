# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    RedundantComparisonViolation,
)
from wemake_python_styleguide.visitors.ast.comparisons import (
    ComparisonSanityVisitor,
)

create_variables = """
variable = 1
another_variable = 2
{0}
"""


@pytest.mark.parametrize('comparators', [
    ('variable', '"test"'),
    ('variable', 'variable.call()'),
    ('variable', 'len(variable)'),
    ('variable', 'another_variable'),
    ('variable', '222'),
])
def test_not_redundant(
    assert_errors,
    parse_ast_tree,
    simple_conditions,
    comparators,
    default_options,
):
    """Testing that comparisons work well."""
    tree = parse_ast_tree(
        create_variables.format(simple_conditions.format(*comparators)),
    )

    visitor = ComparisonSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', [
    ('variable', 'variable'),
    ('another_variable', 'another_variable'),
])
def test_redundant(
    assert_errors,
    parse_ast_tree,
    simple_conditions,  # TODO: use lazy fixture to test `in` conditions
    comparators,
    default_options,
):
    """Testing that violations are when comparing identical variable."""
    tree = parse_ast_tree(
        create_variables.format(simple_conditions.format(*comparators)),
    )

    visitor = ComparisonSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantComparisonViolation])


def test_multiple_compare(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Ensuring than multiple redundant compare returns a single violation."""
    tree = parse_ast_tree('assert some == some == some')

    visitor = ComparisonSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantComparisonViolation])

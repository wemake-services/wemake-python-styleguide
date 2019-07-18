# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    NegatedConditionsViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor

simple_conditions = """
if {0}:
    ...
"""

complex_conditions = """
if {0}:
    ...
else:
    ...
"""


@pytest.mark.parametrize('code', [
    'not some',
    '-some',
    'some != 1',
    'some',
    'some == 0',
    'some != other',
    'some > 1',
])
def test_negated_simple_conditions(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing simple conditions."""
    tree = parse_ast_tree(simple_conditions.format(code))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'not some',
    'some != 1',
    'some != other',
])
def test_wrong_negated_complex_conditions(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing complex conditions with nagated ``if`` condition."""
    tree = parse_ast_tree(complex_conditions.format(code))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NegatedConditionsViolation])


@pytest.mark.parametrize('code', [
    'some',
    '-some',
    '~some',
    'some == 0',
    'some > -1',
    'some < other',
])
def test_correctly_negated_complex_conditions(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing correctly negated complex conditions."""
    tree = parse_ast_tree(complex_conditions.format(code))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

import pytest

from wemake_python_styleguide.violations.refactoring import (
    NegatedConditionsViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor

if_expression = '1 if {0} else 2'
simple_conditions = """
if {0}:
    ...
"""

complex_elif_conditions = """
if {0}:
    ...
elif ...:
    ...
"""

complex_conditions = """
if {0}:
    ...
else:
    ...
"""

complex_elif_else_conditions = """
if {0}:
    ...
elif ...:
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
    '-some',
    'some != 1',
    'some',
    'some == 0',
    'some != other',
    'some > 1',
])
def test_negated_complex_elif_conditions(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing complex conditions without else expression."""
    tree = parse_ast_tree(complex_elif_conditions.format(code))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    if_expression,
    complex_conditions,
    complex_elif_else_conditions,
])
@pytest.mark.parametrize('code', [
    'not some',
    'some != 1',
    'some != other',
])
def test_wrong_negated_complex_conditions(
    code,
    template,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing complex conditions with negated ``if`` condition."""
    tree = parse_ast_tree(template.format(code))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NegatedConditionsViolation])


@pytest.mark.parametrize('template', [
    complex_conditions,
    complex_elif_else_conditions,
])
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
    template,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing correctly negated complex conditions."""
    tree = parse_ast_tree(template.format(code))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

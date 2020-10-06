import pytest

from wemake_python_styleguide.violations.refactoring import (
    SimplifiableIfViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongConditionalVisitor,
)

if_expression = '{0} if some() else {1}'

conditional_statement = """
if some_condition:
    {0}
else:
    {1}
"""

early_returning_conditional_statement = """
if some_condition:
    {0}
{1}
"""

not_simplifiable_comparators = [
    ('variable', '"test"'),
    ('12', 'variable.call()'),
    ('False', 'len(variable)'),
    ('False', 'None'),
    ('True', '222'),
    ('True', 'None'),
]

simplifiable_comparators = [
    ('True', 'False'),
    ('False', 'True'),
]


@pytest.mark.parametrize('comparators', not_simplifiable_comparators)
def test_not_simplifiable_exp(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """Testing that compares work well."""
    tree = parse_ast_tree(if_expression.format(*comparators))

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', simplifiable_comparators)
def test_simplifiable_exp(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """Testing that compares can be simplified."""
    tree = parse_ast_tree(if_expression.format(*comparators))

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [SimplifiableIfViolation])


@pytest.mark.parametrize('comparators', simplifiable_comparators)
def test_simplifiable_conditional_statement(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options
):
    """Test that the conditional statements can be simplified to just returning the condition."""
    tree = parse_ast_tree(conditional_statement.format(*comparators))

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [SimplifiableIfViolation])


@pytest.mark.parametrize('comparators', not_simplifiable_comparators)
def test_not_simplifiable_conditional_statement(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options
):
    """
    Test that the conditional statements can not be simplified to just returning the condition.
    """
    tree = parse_ast_tree(conditional_statement.format(*comparators))

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', simplifiable_comparators)
def test_simplifiable_early_returning_conditional_statement(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options
):
    """
    Test that the early returning conditional statements can be simplified to just returning the
    condition.
    """
    tree = parse_ast_tree(conditional_statement.format(*comparators))

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [SimplifiableIfViolation])


@pytest.mark.parametrize('comparators', not_simplifiable_comparators)
def test_not_simplifiable_early_returning_conditional_statement(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options
):
    """
    Test that the early returning conditional statements can not be simplified to just returning the
    condition.
    """
    tree = parse_ast_tree(conditional_statement.format(*comparators))

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

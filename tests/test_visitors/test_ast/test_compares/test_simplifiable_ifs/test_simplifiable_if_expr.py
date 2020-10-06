import pytest

from wemake_python_styleguide.violations.refactoring import (
    SimplifiableIfViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongConditionalVisitor,
)

if_expression = '{0} if some() else {1}'

conditional_statement = """
def some_function():
    if some_condition:
        return {0}
    else:
        return {1}
"""

not_simplifiable_conditional_statement_if = """
def some_function():
    if some_condition:
        a = 1
        return {0}
    else:
        return {1}
"""

not_simplifiable_conditional_statement_else = """
def some_function():
    if some_condition:
        return {0}
    else:
        a = 1
        return {1}
"""

early_returning_conditional_statement = """
def some_function():
    if some_condition:
        return {0}
    return {1}
"""

not_simplifiable_early_returning_conditional_statement_inside = """
def some_function():
    if some_condition:
        a = 1
        return {0}
    return {1}
"""

not_simplifiable_early_returning_conditional_statement_outside = """
def some_function():
    if some_condition:
        return {0}
    a = 1
    return {1}
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
    """
    Test that the conditional statements can be simplified to just
    returning the condition.
    """
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
    Test that the conditional statements can not be simplified to just
    returning the condition.
    """
    tree = parse_ast_tree(conditional_statement.format(*comparators))

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', simplifiable_comparators)
def test_not_simplifiable_conditional_statement_if(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options
):
    """
    Test that the conditional statements can not be simplified because
    there is extra code in the if part.
    """
    tree = parse_ast_tree(
        not_simplifiable_conditional_statement_if.format(*comparators)
    )

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', simplifiable_comparators)
def test_not_simplifiable_conditional_statement_else(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options
):
    """
    Test that the conditional statements can not be simplified because
    there is extra code in the else part.
    """
    tree = parse_ast_tree(
        not_simplifiable_conditional_statement_else.format(*comparators)
    )

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
    Test that the early returning conditional statements can be simplified
    to just returning the condition.
    """
    tree = parse_ast_tree(
        early_returning_conditional_statement.format(*comparators)
    )

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
    Test that the early returning conditional statements can not be simplified
    to just returning the condition.
    """
    tree = parse_ast_tree(
        early_returning_conditional_statement.format(*comparators)
    )

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', simplifiable_comparators)
def test_not_simplifiable_early_returning_conditional_statement_inside(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options
):
    """
    Test that the early returning conditional statements can not be simplified
    to just returning the condition because there is extra code in the if part.
    """
    tree = parse_ast_tree(
        not_simplifiable_early_returning_conditional_statement_inside.format(
            *comparators
        )
    )

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', simplifiable_comparators)
def test_not_simplifiable_early_returning_conditional_statement_outside(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options
):
    """
    Test that the early returning conditional statements can not be simplified
    to just returning the condition because there is extra code in the if part.
    """
    tree = parse_ast_tree(
        not_simplifiable_early_returning_conditional_statement_outside.format(
            *comparators
        )
    )

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

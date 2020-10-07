import pytest

from wemake_python_styleguide.violations.refactoring import (
    SimplifiableReturningIfStatementViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongReturningConditionalStatementVisitor,
)

simple_if_function = """
def some_function():
    if some_condition:
        return {0}
    else:
        return {1}
"""

simple_early_returning_if = """
def some_function():
    if some_condition:
        return {0}
    return {1}
"""


@pytest.mark.parametrize('comparators', [
    ('True', 'False'),
    ('False', 'True'),
])
def test_simplifiable_if(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """These if statements are simplifiable."""
    tree = parse_ast_tree(simple_if_function.format(*comparators))

    visitor = WrongReturningConditionalStatementVisitor(
        default_options,
        tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [SimplifiableReturningIfStatementViolation])


@pytest.mark.parametrize('comparators', [
    ('True', 'False'),
    ('False', 'True'),
])
def test_simplifiable_early_returning_if(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """These early returning ifs are simplifiable."""
    tree = parse_ast_tree(simple_early_returning_if.format(*comparators))

    visitor = WrongReturningConditionalStatementVisitor(
        default_options,
        tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [SimplifiableReturningIfStatementViolation])

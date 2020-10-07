import pytest

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

complex_if_function_if = """
def some_function():
    if some_condition:
        a = 1
        return {0}
    else:
        return {1}
"""

complex_if_function_else = """
def some_function():
    if some_condition:
        return {0}
    else:
        a = 1
        return {1}
"""

complex_early_returning_if_inside = """
def some_function():
    if some_condition:
        a = 1
        return {0}
    return {1}
"""

complex_early_returning_if_outside = """
def some_function():
    if some_condition:
        return {0}
    a = 1
    return {1}
"""


@pytest.mark.parametrize('comparators', [
    ('variable', '"test"'),
    ('12', 'variable.call()'),
    ('False', 'len(variable)'),
    ('False', 'None'),
    ('True', '222'),
    ('True', 'None'),
])
def test_complex_if(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """The if statement can not be simplified."""
    tree = parse_ast_tree(simple_if_function.format(*comparators))

    visitor = WrongReturningConditionalStatementVisitor(
        default_options,
        tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', [
    ('True', 'False'),
    ('False', 'True'),
])
def test_complex_if_if(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """More complex code in if statements can not be simplified (if)."""
    tree = parse_ast_tree(complex_if_function_if.format(*comparators))

    visitor = WrongReturningConditionalStatementVisitor(
        default_options,
        tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', [
    ('True', 'False'),
    ('False', 'True'),
])
def test_complex_if_else(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """More complex code in if statements can not be simplified (else)."""
    tree = parse_ast_tree(complex_if_function_else.format(*comparators))

    visitor = WrongReturningConditionalStatementVisitor(
        default_options,
        tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', [
    ('variable', '"test"'),
    ('12', 'variable.call()'),
    ('False', 'len(variable)'),
    ('False', 'None'),
    ('True', '222'),
    ('True', 'None'),
])
def test_complex_early_returning_if(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """These early returning ifs can not be simplified."""
    tree = parse_ast_tree(simple_early_returning_if.format(*comparators))

    visitor = WrongReturningConditionalStatementVisitor(
        default_options,
        tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', [
    ('True', 'False'),
    ('False', 'True'),
])
def test_complex_early_returning_if_inside(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """These more complex early returning ifs can not be simplified (inside)."""
    tree = parse_ast_tree(
        complex_early_returning_if_inside.format(*comparators),
    )

    visitor = WrongReturningConditionalStatementVisitor(
        default_options,
        tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', [
    ('True', 'False'),
    ('False', 'True'),
])
def test_complex_early_returning_if_outside(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """These early returning ifs can not be simplified (outside)."""
    tree = parse_ast_tree(
        complex_early_returning_if_outside.format(*comparators),
    )

    visitor = WrongReturningConditionalStatementVisitor(
        default_options,
        tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [])

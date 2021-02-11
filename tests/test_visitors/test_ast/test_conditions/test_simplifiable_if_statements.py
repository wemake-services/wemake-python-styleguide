import pytest

from wemake_python_styleguide.violations.refactoring import (
    SimplifiableReturningIfViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor

complex_else = """
def some_function():
    if some_condition:
        return {0}
    else:
        a = 1
        return {1}
"""

simple_early_returning_if = """
def some_function():
    if some_condition:
        return {0}
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

elif_statement = """
def some_function():
    if some_condition:
        return {0}
    elif other_condition:
        return {1}
    else:
        return {2}
"""

only_if = """
def some_function():
    if some_condition:
        return {0}
"""


@pytest.mark.parametrize('comparators', [
    ('variable', '"test"'),
    ('12', 'variable.call()'),
    ('False', 'len(variable)'),
    ('True', '222'),
])
def test_complex_early_returning_if(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """These early returning ifs can not be simplified."""
    tree = parse_ast_tree(simple_early_returning_if.format(*comparators))

    visitor = IfStatementVisitor(
        default_options,
        tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    complex_early_returning_if_inside,
    complex_early_returning_if_outside,
])
@pytest.mark.parametrize('comparators', [
    ('True', 'False'),
    ('False', 'True'),
])
def test_complex_early_returning_if_inside(
    assert_errors,
    parse_ast_tree,
    template,
    comparators,
    default_options,
):
    """These more complex early returning ifs can not be simplified."""
    tree = parse_ast_tree(template.format(*comparators))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


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

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [SimplifiableReturningIfViolation])


@pytest.mark.parametrize('comparators', [
    ('True', 'False'),
    ('False', 'True'),
])
def test_complex_else(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """This if is not simplifiable, although the else is useless."""
    tree = parse_ast_tree(complex_else.format(*comparators))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', [
    ('True', 'False', 'True'),
    ('False', 'True', 'True'),
])
def test_not_simplifiable_elif(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """Statements with elif are not simplifiable."""
    tree = parse_ast_tree(elif_statement.format(*comparators))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', [
    ('True', ),
    ('False', ),
])
def test_not_simplifiable_only_if(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """Statements with only if and empty parent are not simplifiable."""
    tree = parse_ast_tree(only_if.format(*comparators))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

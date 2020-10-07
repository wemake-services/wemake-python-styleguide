import pytest

from wemake_python_styleguide.violations.refactoring import (
    SimplifiableIfViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongConditionalVisitor,
)

if_expression = '{0} if some() else {1}'


@pytest.mark.parametrize('comparators', [
    ('variable', '"test"'),
    ('12', 'variable.call()'),
    ('False', 'len(variable)'),
    ('False', 'None'),
    ('True', '222'),
    ('True', 'None'),
])
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


@pytest.mark.parametrize('comparators', [
    ('True', 'False'),
    ('False', 'True'),
])
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

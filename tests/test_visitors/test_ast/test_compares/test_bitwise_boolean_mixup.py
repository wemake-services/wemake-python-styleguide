import pytest

from wemake_python_styleguide.violations.best_practices import (
    BitwiseAndBooleanMixupViolation,
)
from wemake_python_styleguide.visitors.ast.compares import BitwiseOpVisitor

# add more cases for more usages of mixup


@pytest.mark.parametrize('expression', [
    'True | False',
    '(x >= y) & True',
    '(x > 5) | (10 == second)',
    '(11 != first) | (not False)',
    '(1 or first) & (second and first)',
])
def test_bitwise_boolean_mixup(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing for forbidden comparison between bitwise and boolean operator."""
    tree = parse_ast_tree(expression)

    visitor = BitwiseOpVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BitwiseAndBooleanMixupViolation])


@pytest.mark.parametrize('expression', [
    'x | y',
    'y & x',
    'first & second',
    '5 | 10',
    '5 | x',
])
def test_correct_binary(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing allowed bitwise comparisions."""
    tree = parse_ast_tree(expression)

    visitor = BitwiseOpVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

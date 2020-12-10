import pytest

from wemake_python_styleguide.violations.best_practices import (
    ListMultiplyViolation,
)
from wemake_python_styleguide.visitors.ast.operators import (
    WrongMathOperatorVisitor,
)
# replace with my finished vistor and violations

usage_template = 'constant = {0}'

# add more cases for more usages of mixup

@pytest.mark.parametrize('expression', [
    'True | False',
    '(x >= y) & True',
])
def test_bitwise_boolean_mixup(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing for forbidden comparison between bitwise and boolean operator"""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = WrongMathOperatorVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ListMultiplyViolation])


@pytest.mark.parametrize('expression', [
    'x | y',
    'y & x',
])
def test_correct_binary(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing allowed bitwise comparisions"""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = WrongMathOperatorVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

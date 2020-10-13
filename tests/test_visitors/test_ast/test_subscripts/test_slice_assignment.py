import pytest

from wemake_python_styleguide.violations.consistency import (
    AssignToSliceViolation,
)
from wemake_python_styleguide.visitors.ast.subscripts import SubscriptVisitor

usage_template = 'constant[{0}]= [1, 2, 3]'


@pytest.mark.parametrize('expression', [
    ':7',
    '1:7:2',
    '3:',
    '3::',
    '::2',
    ':2:',
    ':',
    'slice(1)',
    'slice()',
    'slice(1,3)',
])
def test_slice_assignment(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that slice assignments are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SubscriptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [AssignToSliceViolation])


@pytest.mark.parametrize('expression', [
    '5',
])
def test_regular_index_assignment(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that regular index assignment is allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SubscriptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

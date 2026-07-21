import pytest

from wemake_python_styleguide.violations.consistency import (
    AssignToSliceViolation,
)
from wemake_python_styleguide.visitors.ast.subscripts import SubscriptVisitor

usage_template = 'constant[{0}] = [1, 2, 3]'


@pytest.mark.parametrize(
    'expression',
    [
        ':7',
        '1:7:2',
        '3:',
        '::2',
        ':2:',
        ':',
        'slice(1)',
        'slice()',
        'slice(1, 3)',
    ],
)
def test_slice_assignment(
    assert_errors,
    parse_ast_tree,
    parse_tokens,
    expression,
    default_options,
):
    """Testing that slice assignments are forbidden."""
    code = usage_template.format(expression)
    tree = parse_ast_tree(code)
    tokens = parse_tokens(code)

    visitor = SubscriptVisitor(default_options, tree=tree, file_tokens=tokens)
    visitor.run()

    assert_errors(visitor, [AssignToSliceViolation])


@pytest.mark.parametrize(
    'expression',
    [
        '5',
        '"string"',
        'object',
        'dict[key]',
        'subslice[1:2]',
        'func(1, 2)',
    ],
)
def test_regular_index_assignment(
    assert_errors,
    parse_ast_tree,
    parse_tokens,
    expression,
    default_options,
):
    """Testing that regular index assignment is allowed."""
    code = usage_template.format(expression)
    tree = parse_ast_tree(code)
    tokens = parse_tokens(code)

    visitor = SubscriptVisitor(default_options, tree=tree, file_tokens=tokens)
    visitor.run()

    assert_errors(visitor, [])

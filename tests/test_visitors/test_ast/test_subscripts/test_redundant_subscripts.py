import pytest

from wemake_python_styleguide.violations.consistency import (
    RedundantSubscriptViolation,
)
from wemake_python_styleguide.visitors.ast.subscripts import SubscriptVisitor

usage_template = 'constant[{0}]'


@pytest.mark.parametrize(
    'expression',
    [
        '0:7',
        'None:7',
        '3:None',
        '3:None:2',
        '3:7:None',
        '3:7:1',
    ],
)
def test_one_redundant_subscript(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that redundant subscripts are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SubscriptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantSubscriptViolation])


@pytest.mark.parametrize(
    'expression',
    [
        '0:7:1',
        '0:7:None',
        '0:None',
        'None:7:None',
        'None:None',
        '3:None:1',
        ':None:None',
    ],
)
def test_two_redundant_subscript(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that redundant subscripts are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SubscriptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [
            RedundantSubscriptViolation,
            RedundantSubscriptViolation,
        ],
    )


@pytest.mark.parametrize(
    'expression',
    [
        '0:None:1',
        'None:None:1',
        'None:None:None',
        '0:None:None',
    ],
)
def test_three_redundant_subscript(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that redundant subscripts are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SubscriptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [
            RedundantSubscriptViolation,
            RedundantSubscriptViolation,
            RedundantSubscriptViolation,
        ],
    )


@pytest.mark.parametrize(
    'expression',
    [
        '5',
        '3:7',
        '3:7:2',
        '3:',
        ':7',
        '3::2',
        '3:7:',
        ':7:2',
        '3::',
        ':7:',
        '::2',
        ':',
        '::',
    ],
)
def test_correct_subscripts(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that non-redundant subscripts are allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SubscriptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

import pytest

from wemake_python_styleguide.violations.refactoring import (
    NegatedConditionsViolation,
    UselessTernaryViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor

template = '{0} if {1} else {2}'


@pytest.mark.parametrize(
    ('left', 'compare', 'right'),
    [
        ('x', 'condition', 'y'),
        ('x', 'x > y', 'y'),
        ('x', 'x == y and y > 0', 'y'),
        ('2', 'x == y', 'call().attr'),
        ('a', 'x == y', 'b'),
        ('x[0]', 'x == y', 'x[1]'),
        ('x[0]', 'x[0] == y[1]', 'y[0]'),
        ('a.x', 'x == y', 'b.y'),
        ('call.method()', 'x != y', 'obj.attr'),
    ],
)
def test_useful_ternary(
    assert_errors,
    parse_ast_tree,
    left,
    compare,
    right,
    default_options,
):
    """Testing that correct code works."""
    tree = parse_ast_tree(template.format(left, compare, right))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [], ignored_types=NegatedConditionsViolation)


@pytest.mark.parametrize(
    ('left', 'compare', 'right'),
    [
        ('x', 'x == y', 'y'),
        ('[x]', '[x] == [y]', '[y]'),
        ('{x}', '{x} == {y}', '{y}'),
        ('(x,)', '(x,) == (y,)', '(y,)'),
        ('x.a', 'x.a == y.b', 'y.b'),
        ('x.a', 'x.a is None', 'None'),
        ('None', 'x[0] is None', 'x[0]'),
        ('False', 'x[0] is False', 'x[0]'),
        ('x[0]', 'x[0] is not None', 'None'),
        ('x.attr[0]', 'x.attr[0] != y.b', 'y.b'),
    ],
)
def test_useless_ternary(
    assert_errors,
    parse_ast_tree,
    left,
    compare,
    right,
    default_options,
):
    """Testing that incorrect code raises a violation."""
    tree = parse_ast_tree(template.format(left, compare, right))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [UselessTernaryViolation],
        ignored_types=NegatedConditionsViolation,
    )

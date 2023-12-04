import pytest

from wemake_python_styleguide.violations.refactoring import (
    FalsyConstantCompareViolation,
    WrongIsCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongConstantCompareVisitor,
)

wrong_comparators = [
    ('some', '[]'),
    ('some', '{}'),  # noqa: P103
    ('some', '()'),
    ('[]', 'some'),
    ('{}', 'some'),  # noqa: P103
    ('()', 'some'),

    ('some', '(x := [])'),
    ('(x := [])', 'some'),
]


@pytest.mark.parametrize('comparators', wrong_comparators)
def test_falsy_constant(
    assert_errors,
    parse_ast_tree,
    comparators,
    eq_conditions,
    default_options,
):
    """Testing that compares with falsy constants are not allowed."""
    tree = parse_ast_tree(eq_conditions.format(*comparators))

    visitor = WrongConstantCompareVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [FalsyConstantCompareViolation])


@pytest.mark.filterwarnings('ignore::SyntaxWarning')
@pytest.mark.parametrize('comparators', wrong_comparators)
def test_falsy_constant_is(
    assert_errors,
    parse_ast_tree,
    comparators,
    is_conditions,
    default_options,
):
    """Testing that compares with falsy constants are not allowed."""
    tree = parse_ast_tree(is_conditions.format(*comparators))

    visitor = WrongConstantCompareVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        FalsyConstantCompareViolation,
        WrongIsCompareViolation,
    ])


@pytest.mark.parametrize('comparators', wrong_comparators)
def test_falsy_constant_not_eq(
    assert_errors,
    parse_ast_tree,
    comparators,
    other_conditions,
    default_options,
):
    """Testing that compares with falsy constants are not allowed."""
    tree = parse_ast_tree(other_conditions.format(*comparators))

    visitor = WrongConstantCompareVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.filterwarnings('ignore::SyntaxWarning')
@pytest.mark.parametrize('comparators', [
    ('some', '[1, 2]'),
    ('some', '{1, 2}'),
    ('some', '{"1": 2}'),
    ('some', '(1, 2)'),
    ('some', 'None'),
    ('some', 'False'),
    ('some', 'True'),
    ('some', '0'),
    ('some', '1'),
    ('some', '""'),
    ('some', '"a"'),
    ('some', 'b"bytes"'),
    ('some', 'other'),
    ('some', 'other()'),
    ('some', 'other.attr'),
    ('some', 'other.method()'),
    ('some', 'other[0]'),
    ('None', 'some'),
    ('(x := [1, 2])', 'some'),
])
def test_correct_constant_compare(
    assert_errors,
    parse_ast_tree,
    comparators,
    simple_conditions,
    default_options,
):
    """Testing that normal compares are allowed."""
    tree = parse_ast_tree(simple_conditions.format(*comparators))

    visitor = WrongConstantCompareVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [], ignored_types=WrongIsCompareViolation)

import pytest

from wemake_python_styleguide.violations.refactoring import (
    FalsyConstantCompareViolation,
    WrongIsCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongConstantCompareVisitor,
)

wrong_comparators = [
    ('some', '[1, 2]'),
    ('some', '{}'),  # noqa: P103
    ('some', '()'),
    ('some', '{1, 2, 3}'),

    ('some', '[x for x in a]'),
    ('some', '(x for x in a)'),
    ('some', '{x for x in a}'),
    ('some', '{"1": x for x in a}'),

    ('some', '0'),
    ('some', '1'),
    ('some', '1.2'),
    ('some', '-0.1'),
    ('some', '""'),
    ('some', '"abc"'),
    ('some', 'b"bytes"'),

    ('some', '(1, 2)'),
    ('[]', 'some'),
    ('{1, 2}', 'some'),
    ('()', 'some'),
    ('"test"', 'some'),

    ('(x := some())', '"abc"'),
    ('(x := "abc")', 'some()'),
]


@pytest.mark.filterwarnings('ignore::SyntaxWarning')
@pytest.mark.parametrize('comparators', wrong_comparators)
def test_wrong_constant_is(
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

    assert_errors(
        visitor,
        [WrongIsCompareViolation],
        ignored_types=FalsyConstantCompareViolation,
    )


@pytest.mark.parametrize('comparators', [
    ('some', 'None'),
    ('some', 'False'),
    ('some', 'True'),
    ('None', 'some'),

    ('some', 'other'),
    ('some', 'x + y'),
    ('some', 'other.attr'),
    ('some', 'call()'),
    ('some', 'other.method'),
    ('some', 'other[key]'),
    ('some', 'some'),
])
def test_correct_constant_is(
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

    assert_errors(visitor, [])

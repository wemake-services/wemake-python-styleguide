import pytest

from wemake_python_styleguide.violations.consistency import (
    CompareOrderViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongComparisonOrderVisitor,
)

wrong_comparators = [
    ('"string constant"', 'first_name'),
    ([1, 2, 3], 'first_name'),
    (1, 'len(first_name)'),
    (1, 'first_name.call()'),
    (1, 'first_name + 10'),
    (1, 'first_name + second_name'),

    ('1', '(x := first())'),
    ('(x := 1)', 'first()'),
]


regression577 = """
async def function():
    assert await _coroutine(1) == Success(1)
"""


@pytest.mark.filterwarnings('ignore::SyntaxWarning')
@pytest.mark.parametrize('comparators', [
    ('first_name', 'second_name'),
    ('first_name', 'second_name + 1'),
    ('first_name', '"string constant"'),
    ('first_name', [1, 2, 3]),
    ('first_name', 'len(second_name)'),
    ('len(first_name)', 1),
    ('first_name.call()', 1),
    ('first_name.attr', 1),
    ('first_name + 10', 1),
    ('first_name + second_name', 1),
    ('error.code', 'errors[index].code'),
    (1, 2),
    ('returned_item["id"]', 'office.id'),
    ('(x := first(1, 2))', '"str"'),
])
def test_compare_variables(
    assert_errors,
    parse_ast_tree,
    simple_conditions,
    comparators,
    default_options,
):
    """Compares work well for left variables."""
    tree = parse_ast_tree(simple_conditions.format(*comparators))

    visitor = WrongComparisonOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', [
    ('"string constant"', 'container'),
    ('container', '"string constant"'),
    ('(x := first(1, 2))', '"str"'),
])
def test_compare_variables_in_special_case(
    assert_errors,
    parse_ast_tree,
    in_conditions,
    comparators,
    default_options,
):
    """Ensures that special case for `in` and `not in` is handled."""
    tree = parse_ast_tree(in_conditions.format(*comparators))

    visitor = WrongComparisonOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.filterwarnings('ignore::SyntaxWarning')
@pytest.mark.parametrize('comparators', wrong_comparators)
def test_compare_wrong_order(
    assert_errors,
    parse_ast_tree,
    simple_conditions,
    comparators,
    default_options,
):
    """Compares raise for left constants."""
    tree = parse_ast_tree(simple_conditions.format(*comparators))

    visitor = WrongComparisonOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [CompareOrderViolation])


@pytest.mark.parametrize('comparators', wrong_comparators)
def test_compare_wrong_order_multiple(
    assert_errors,
    parse_ast_tree,
    comparators,
    default_options,
):
    """Compares raise multiple issues for left constants."""
    tree = parse_ast_tree(
        'if {0} > {1} and {0} < {1}: ...'.format(*comparators),
    )

    visitor = WrongComparisonOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        CompareOrderViolation,
        CompareOrderViolation,
    ])


def test_compare_wrong_order_regression577(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """
    Ensures that `await` can be used in a comparison.

    See: https://github.com/wemake-services/wemake-python-styleguide/issues/577
    """
    tree = parse_ast_tree(regression577)

    visitor = WrongComparisonOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

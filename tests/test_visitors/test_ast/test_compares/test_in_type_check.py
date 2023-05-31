import pytest

from wemake_python_styleguide.violations.refactoring import (
    InCompareWithSingleItemContainerViolation,
    WrongInCompareTypeViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    InCompareSanityVisitor,
)

in_template = 'some in {0}'
not_in_template = 'some not in {0}'


@pytest.mark.parametrize('code', [
    not_in_template,
    in_template,
])
@pytest.mark.parametrize('comparator', [
    '[]',
    '[1, 2, 3]',
    '[x for x in call()]',
    {},
    '{"x": x for x in call()}',
    '{"x": 1}',
    '()',
    '(1, 2, 3)',
    '(x for x in call())',
    '(x := [1, 2, 3])',
])
def test_compare_with_wrong_type(
    assert_errors,
    parse_ast_tree,
    code,
    comparator,
    default_options,
):
    """Compares raise a violation for ``in`` with wrong types."""
    tree = parse_ast_tree(code.format(comparator))

    visitor = InCompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [WrongInCompareTypeViolation],
        ignored_types=InCompareWithSingleItemContainerViolation,
    )


@pytest.mark.parametrize('code', [
    not_in_template,
    in_template,
])
@pytest.mark.parametrize('comparator', [
    '{1, 2}',
    '{x for x in call()}',
    'set()',
    'name',
    'method.call()',
    'prop.attr',
])
def test_compare_with_correct_type(
    assert_errors,
    parse_ast_tree,
    code,
    comparator,
    default_options,
):
    """Compares work correctly for ``in`` with correct types."""
    tree = parse_ast_tree(code.format(comparator))

    visitor = InCompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

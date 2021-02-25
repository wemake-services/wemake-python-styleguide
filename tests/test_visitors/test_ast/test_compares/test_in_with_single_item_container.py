import pytest

from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.violations.refactoring import (
    InCompareWithSingleItemContainerViolation,
    WrongInCompareTypeViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    InCompareSanityVisitor,
)


@pytest.mark.parametrize('code', [
    'a in {1}',
    'a in {1: "a"}',
    'a in [1]',
    'a in (1,)',
    'a in "a"',
    'a in b"a"',
    'a in {*a}',
    'a in {**a}',
    pytest.param(
        'a in (x := [1])',
        marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8'),
    ),
])
def test_single_item_container(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    in_not_in,
):
    """Compares forbid ``in`` with single item containers."""
    tree = parse_ast_tree(code)

    visitor = InCompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [InCompareWithSingleItemContainerViolation],
        ignored_types=WrongInCompareTypeViolation,
    )


@pytest.mark.parametrize('code', [
    'a in {1, 2}',
    'a in {1: "a", 2: "b"}',
    'a in [1, 2]',
    'a in (1, 2)',
    'a in "ab"',
    'a in {1, *a}',
    'a in {1: "a", **a}',
    pytest.param(
        'a in (x := {1, 2, 3})',
        marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8'),
    ),
])
def test_multi_item_container(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    in_not_in,
):
    """Compares allow ``in`` with multi items containers."""
    tree = parse_ast_tree(code)

    visitor = InCompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [], ignored_types=WrongInCompareTypeViolation)

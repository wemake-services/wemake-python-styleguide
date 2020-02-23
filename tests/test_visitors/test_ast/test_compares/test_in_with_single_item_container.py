# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    InCompareWithSingleItemContainerViolation,
    WrongInCompareTypeViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    InCompareSanityVisitor,
)


@pytest.mark.parametrize('code', [
    'if a in {1}: ...',
    'if a in {1: "a"}: ...',
    'if a in [1]: ... ',
    'if a in (1,): ... ',
    'if a in "a": ... ',
    'if a in {*a}: ... ',
    'if a in {**a}: ... ',
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
        ignored_types=(WrongInCompareTypeViolation,),
    )


@pytest.mark.parametrize('code', [
    'if a in {1, 2}: ...',
    'if a in {1: "a", 2: "b"}: ...',
    'if a in [1, 2]: ... ',
    'if a in (1, 2): ... ',
    'if a in "ab": ... ',
    'if a in {1, *a}: ... ',
    'if a in {1: "a", **a}: ... ',
])
def test_multi_item_contrainer(
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

    assert_errors(
        visitor,
        [],
        ignored_types=(WrongInCompareTypeViolation,),
    )

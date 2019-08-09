# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    PointlessStarredViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    PointlessStarredVisitor,
)


@pytest.mark.parametrize('code', [
    'print(*[])',
    'print(*())',
    'print(*{})',  # noqa: P103
    'print(**{})',  # noqa: P103
    'print(*[1, 2])',
    'print(*(1, 2))',
    'print(*{1, 2})',
    'print(**{"end": " "})',
])
def test_pointless_starred_arg(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that pointless starred expression is detected."""
    tree = parse_ast_tree(code)

    visitor = PointlessStarredVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [PointlessStarredViolation])


@pytest.mark.parametrize('code', [
    'print(*[], **{})',  # noqa: P103
    'print(*[], **{"1": 1})',  # noqa: P103
    'print(*[1], **{})',
    'print(*[1], **{"end": " "})',
])
def test_pointless_starred_arg_and_keyword(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that pointless starred expression is detected."""
    tree = parse_ast_tree(code)

    visitor = PointlessStarredVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [PointlessStarredViolation, PointlessStarredViolation],
    )


@pytest.mark.parametrize('code', [
    """
    _list = [1, 2]
    _dict = {"end": " "}
    print(*_list, **_dict)
    """,
])
def test_useful_starred_arg_and_keyword(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that pointless starred expression is detected."""

    tree = parse_ast_tree(code)

    visitor = PointlessStarredVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

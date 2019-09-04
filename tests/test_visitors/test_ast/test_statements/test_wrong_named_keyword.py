# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    WrongNamedKeywordViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    WrongNamedKeywordVisitor,
)


@pytest.mark.parametrize('code', [
    'print(**{"@": "2"})',
    'print(**{"2ab": "2"})',
    'print(end="|", **{"2ab": "2"})',
])
def test_wrong_starred_keyword(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that pointless starred expression is detected."""
    tree = parse_ast_tree(code)

    visitor = WrongNamedKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongNamedKeywordViolation])


@pytest.mark.parametrize('code', [
    '_list = [1, 2]',
    '_dict = {"end": " "}',
    'print(*_list, **_dict)',
    'print(end="1", **{"a": 1})',
    'filter(**{User.USERNAME_FIELD: username})',  # noqa: P103
    'filter(**{"a2": 1, _: 2})',
    'filter(**{"a": 1, b: 2})',
    'filter(**{"a": 1, call(): 2})',
    'filter(**{"a": 1, b.method(): 2})',
    'filter(**{b["a"]: 2})',
])
def test_correct_starred_keyword(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that pointless starred expression is detected."""
    tree = parse_ast_tree(code)

    visitor = WrongNamedKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

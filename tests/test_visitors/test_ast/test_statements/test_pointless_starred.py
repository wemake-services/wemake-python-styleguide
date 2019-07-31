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
    'print(*{})',
    'print(*[1], **{})'
])
def test_pointless_starred(
    assert_errors,
    parse_ast_tree,
    default_options,
    code
):
    """Testing that pointless starred expression is detected."""
    tree = parse_ast_tree(code)

    visitor = PointlessStarredVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [PointlessStarredViolation])


@pytest.mark.parametrize('code', [
    'print(*[1, 2, 3])',
    'print(*(1, 2, 3))',
    'print(*{"1": 2})',
])
def test_useful_starred(
    assert_errors,
    parse_ast_tree,
    default_options,
    code
):
    """Testing that pointless starred expression is missing."""
    tree = parse_ast_tree(code)

    visitor = PointlessStarredVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

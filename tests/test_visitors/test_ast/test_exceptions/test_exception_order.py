# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    IncorrectExceptOrderViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongTryExceptVisitor,
)

exception_template = """
try:
    ...
except {0}:
    ...
except {1}:
    ...
"""


@pytest.mark.parametrize('code', [
    exception_template,
])
@pytest.mark.parametrize('statements', [
    ('ValueError', 'Exception'),
])
def test_correct_order_exception(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    statements,
):
    """Testing restrictions are not raised when use correct oder of `except`."""
    tree = parse_ast_tree(code.format(*statements))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    exception_template,
])
@pytest.mark.parametrize('statements', [
    ('Exception', 'ValueError'),
])
def test_wrong_order_exception(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    statements,
):
    """Testing `except Exception:` in the last block is restricted."""
    tree = parse_ast_tree(code.format(*statements))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [IncorrectExceptOrderViolation])

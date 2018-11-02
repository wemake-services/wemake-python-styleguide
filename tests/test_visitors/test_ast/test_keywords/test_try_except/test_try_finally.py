# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    RedundantFinallyViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import WrongTryExceptVisitor

right_try_example = """
try:
    ...
except:
    ...
"""

wrong_try_example = """
try:
    ...
finally:
    ...
"""

check_finally_with_except = """
try:
    ...
except:
    ...
finally:
    ...
"""


@pytest.mark.parametrize('code', [
    wrong_try_example,
])
def test_wrong_finally(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Violations are raised when finally without except in try block."""
    tree = parse_ast_tree(code)

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantFinallyViolation])


@pytest.mark.parametrize('code', [
    right_try_example,
    check_finally_with_except,
])
def test_correct_finally(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Violations are not raised when finally with except in try block."""
    tree = parse_ast_tree(code)

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

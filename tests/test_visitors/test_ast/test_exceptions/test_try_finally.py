# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    UselessFinallyViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongTryExceptVisitor,
)

right_try_example = """
try:
    ...
except:
    ...
"""

wrong_try_example1 = """
try:
    ...
finally:
    ...
"""

wrong_try_example2 = """
def some():
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

check_finally_with_except_else = """
try:
    ...
except Exception:
    ...
else:
    ...
finally:
    ...
"""

# Exceptional cases:

correct_finally_decorated = """
@decorator
def some():
    try:
        ...
    finally:
        ...
"""


@pytest.mark.parametrize('code', [
    wrong_try_example1,
    wrong_try_example2,
])
def test_wrong_finally(
    assert_errors,
    parse_ast_tree,
    code,
    mode,
    default_options,
):
    """Violations are raised when finally without except in try block."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessFinallyViolation])


@pytest.mark.parametrize('code', [
    right_try_example,
    check_finally_with_except,
    check_finally_with_except_else,
    correct_finally_decorated,
])
def test_correct_finally(
    assert_errors,
    parse_ast_tree,
    code,
    mode,
    default_options,
):
    """Violations are not raised when finally with except in try block."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

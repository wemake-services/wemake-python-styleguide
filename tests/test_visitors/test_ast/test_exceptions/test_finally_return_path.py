# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    TryExceptMultipleReturnPathViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongTryExceptVisitor,
)

# Correct:

right_both_return = """
def function():
    try:
        return 1 / 0
    except:
        return 0
"""

right_except_return_else = """
def function():
    try:
        ...
    except:
        return 0
    else:
        return 1
"""

right_else_return = """
def function():
    try:
        ...
    except:
        ...
    else:
        return 0
"""

right_both_return_else = """
def function():
    try:
        return 0
    except:
        return 1
    else:
        ...
"""

right_finally_return = """
def function():
    try:
        ...
    except:
        ...
    finally:
        return 0
"""

right_both_return_finally = """
def function():
    try:
        return 0
    except:
        return 1
    finally:
        ...
"""

# Wrong:

wrong_try_returning = """
def function():
    try:
        return
    except:
        ...
    finally:
        return
"""

wrong_except_return_finally = """
def function():
    try:
        ...
    except:
        return
    finally:
        return
"""

wrong_except_second_return_finally = """
def function():
    try:
        ...
    except TypeError:
        ...
    except Exception:
        return
    finally:
        return
"""

wrong_both_return_finally = """
def function():
    try:
        return
    except:
        return
    finally:
        return
"""

wrong_try_return_else = """
def function():
    try:
        return 0
    except:
        ...
    else:
        return 1
"""

wrong_both_return_else = """
def function():
    try:
        return 0
    except:
        return 1
    else:
        return 2
"""

wrong_both_return_both = """
def function():
    try:
        return 0
    except:
        return 1
    else:
        return 2
    finally:
        return 3
"""


@pytest.mark.parametrize('code', [
    wrong_try_returning,
    wrong_except_return_finally,
    wrong_except_second_return_finally,
    wrong_both_return_finally,
    wrong_try_return_else,
    wrong_both_return_else,
])
def test_wrong_return_in_else_or_finally(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are raised when there are multiple `return` path."""
    tree = parse_ast_tree(code)

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TryExceptMultipleReturnPathViolation])


def test_double_wrong_return_in_else_or_finally(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Two violations are raised when there are multiple `return` path."""
    tree = parse_ast_tree(wrong_both_return_both)

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        TryExceptMultipleReturnPathViolation,
        TryExceptMultipleReturnPathViolation,
    ])


@pytest.mark.parametrize('code', [
    right_both_return,
    right_except_return_else,
    right_else_return,
    right_both_return_else,
    right_finally_return,
    right_both_return_finally,
])
def test_correct_return_path_in_try_except(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are not raised when `return` path is correct."""
    tree = parse_ast_tree(code)

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

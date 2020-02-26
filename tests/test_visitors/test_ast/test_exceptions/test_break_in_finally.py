# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BreakInFinallyBlockViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongTryExceptVisitor,
)

right_try_example = """
def function():
    for element in range(10):
        try:
            ...
        except:
            ...
        finally:
            ...
"""

right_try_example_with_while = """
def function():
    while first_element < second_element:
        try:
            ...
        except:
            ...
        finally:
            ...
"""

right_continue_example_in_for = """
def function():
    def some():
        for elem in range(10):
            if elem > 5:
                break
"""

right_continue_example_in_while = """
def function():
    def some():
        while a < b:
            if a == 5:
                break
"""

wrong_try_example = """
def function():
    for element in range(10):
        try:
            ...
        except:
            ...
        finally:
            break
"""

wrong_try_example_with_while = """
def function():
    while first_element < second_element:
        try:
            ...
        except:
            ...
        finally:
            break
"""


@pytest.mark.parametrize('code', [
    wrong_try_example,
    wrong_try_example_with_while,
])
def test_wrong_finally(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that using `continue` keyword in `break` is not allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BreakInFinallyBlockViolation])


@pytest.mark.parametrize('code', [
    right_try_example,
    right_try_example_with_while,
    right_continue_example_in_for,
    right_continue_example_in_while,
])
def test_correct_finally(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that regular `try` and `break` in loops are allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

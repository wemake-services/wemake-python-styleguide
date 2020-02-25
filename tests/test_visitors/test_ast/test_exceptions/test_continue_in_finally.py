# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.violations.best_practices import (
    ContinueInFinallyBlockViolation,
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
                continue
"""

right_continue_example_in_while = """
def function():
    def some():
        while a < b:
            if a == 5:
                continue
"""

wrong_try_example = """
def function():
    for element in range(10):
        try:
            ...
        except:
            ...
        finally:
            continue
"""

wrong_try_example_with_while = """
def function():
    while first_element < second_element:
        try:
            ...
        except:
            ...
        finally:
            continue
"""


@pytest.mark.skipif(
    not PY38,
    reason='continue in finally works only since python3.8',
)
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
    """Testing that using `continue` keyword in `finally` is not allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ContinueInFinallyBlockViolation])


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
    """Testing that regular `try` `except` `finally` are allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.skipif(
    PY38,
    reason='We check for syntax error here, which is true for python < 3.8',
)
@pytest.mark.parametrize('code', [
    wrong_try_example,
    wrong_try_example_with_while,
])
def test_finally_with_exception(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that using `continue` keyword is not allowed."""
    with pytest.raises(SyntaxError):
        parse_ast_tree(mode(code))

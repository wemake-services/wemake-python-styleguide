import pytest

from wemake_python_styleguide.violations.best_practices import (
    LoopControlFinallyViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongTryExceptVisitor,
)

right_try_example_with_for = """
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

right_example_with_for = """
def function():
    def some():
        for elem in range(10):
            if elem > 5:
                {0}
"""

right_example_with_while = """
def function():
    def some():
        while a < b:
            if a == 5:
                {0}
"""

wrong_try_example = """
def function():
    for element in range(10):
        try:
            ...
        except:
            ...
        finally:
            {0}
"""

wrong_try_example_with_while = """
def function():
    while first_element < second_element:
        try:
            ...
        except:
            ...
        finally:
            {0}
"""


@pytest.mark.parametrize('statement', [
    'break',
    'continue',
])
@pytest.mark.parametrize('code', [
    right_example_with_for,
    right_example_with_while,
    right_try_example_with_for,
    right_try_example_with_while,
])
def test_right_finally(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
    mode,
):
    """Testing that regular loops and loops with `try` are allowed."""
    tree = parse_ast_tree(mode(code.format(statement)))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('statement', [
    'break',
])
@pytest.mark.parametrize('code', [
    wrong_try_example,
    wrong_try_example_with_while,
])
def test_finally_with_break(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
    mode,
):
    """Testing that `break` keyword is not allowed in `finally`."""
    tree = parse_ast_tree(mode(code.format(statement)))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [LoopControlFinallyViolation])


@pytest.mark.parametrize('statement', [
    'continue',
])
@pytest.mark.parametrize('code', [
    wrong_try_example,
    wrong_try_example_with_while,
])
def test_finally_with_continue(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
    mode,
):
    """Testing that `continue` keyword is not allowed in `finally`."""
    tree = parse_ast_tree(mode(code.format(statement)))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [LoopControlFinallyViolation])

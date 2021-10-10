import pytest

from wemake_python_styleguide.violations.best_practices import (
    BareRaiseViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import WrongRaiseVisitor


def test_bare_raise(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing bare raise without except block."""
    code = """
    def bare_raise():
        raise
    """
    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BareRaiseViolation])


def test_bare_raise_wrong_visitor(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that bare `raise` is allowed."""
    code = """
    try:
        1 / 0
    except Exception:
        raise
    """
    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


bare_raise_except_function = """
def bare_raise_with_except():
    try:
        print('test')
    except:
        raise
"""

bare_raise_if_function = """
def bare_raise_with_if():
    try:
        print('test')
    except:
        if 1 == 1:
            raise
"""


@pytest.mark.parametrize('code', [
    bare_raise_except_function,
    bare_raise_if_function,
])
def test_bare_raise_except(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that bare `raise` is only allowed in except blocks."""
    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

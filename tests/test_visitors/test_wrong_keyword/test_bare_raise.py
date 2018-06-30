# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_keyword import (
    BareRiseViolation,
    WrongRaiseVisitor,
)

bare_raise_module = """
raise
"""

bare_raise_function = """
def function():
    raise
"""


@pytest.mark.parametrize('code', [
    bare_raise_module,
    bare_raise_function,
])
def test_bare_raise_keyword(assert_errors, parse_ast_tree, code):
    """Testing that bare raise keyword is restricted outside of except."""
    tree = parse_ast_tree(code)

    visiter = WrongRaiseVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [BareRiseViolation._code])


def test_normal_raise_keyword(assert_errors, parse_ast_tree):
    """Testing that regular bare raise keyword is allowed inside `except`."""
    tree = parse_ast_tree("""
    raise ValueError('Some error')
    """)

    visiter = WrongRaiseVisitor()
    visiter.visit(tree)

    assert visiter.errors == []


def test_bare_raise_in_except_keyword(assert_errors, parse_ast_tree):
    """Testing that regular bare raise keyword is allowed inside `except`."""
    tree = parse_ast_tree("""
    try:
        1 / 0
    except Exception:
        raise
    """)

    visiter = WrongRaiseVisitor()
    visiter.visit(tree)

    assert visiter.errors == []

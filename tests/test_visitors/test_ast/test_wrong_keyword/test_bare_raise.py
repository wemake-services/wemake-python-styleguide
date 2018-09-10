# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.wrong_keyword import (
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
def test_bare_raise_keyword(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that bare raise keyword is restricted outside of except."""
    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BareRiseViolation])


def test_normal_raise_keyword(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that regular bare raise keyword is allowed inside `except`."""
    tree = parse_ast_tree("""
    raise ValueError('Some error')
    """)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_bare_raise_in_except_keyword(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that regular bare raise keyword is allowed inside `except`."""
    tree = parse_ast_tree("""
    try:
        1 / 0
    except Exception:
        raise
    """)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

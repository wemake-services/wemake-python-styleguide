# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.general.wrong_keyword import (
    RaiseNotImplementedViolation,
    WrongRaiseVisitor,
)

raise_not_implemented = """
class CheckAbstractMethods():
    def check_not_implemented(self):
        raise NotImplemented()
"""

raise_not_implemented_type = """
class CheckAbstractMethods():
    def check_not_implemented_without_call(self):
        raise NotImplemented
"""


@pytest.mark.parametrize('code', [
    raise_not_implemented,
    raise_not_implemented_type,
])
def test_raise_not_implemented(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that `raise NotImplemented` is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RaiseNotImplementedViolation])


def test_raise_not_implemented_error(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that `raise NotImplementedError` is allowed."""
    tree = parse_ast_tree('raise NotImplementedError()')

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_bare_raise(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that bare `raise` is allowed."""
    tree = parse_ast_tree("""
    try:
        1 / 0
    except Exception:
        raise
    """)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_keyword import (
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
        raise NotImplemented  # error here
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

    visiter = WrongRaiseVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [RaiseNotImplementedViolation])


def test_raise_not_implemented_error(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that `raise NotImplementedError` is allowed."""
    tree = parse_ast_tree("""
    raise NotImplementedError()
    """)

    visiter = WrongRaiseVisitor(default_options)
    visiter.visit(tree)

    assert visiter.errors == []

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import BAD_MAGIC_METHODS
from wemake_python_styleguide.visitors.wrong_class import (
    BadMagicMethodViolation,
    WrongClassVisitor,
)

magic_method = """
class Example(object):
    def {0}(): ...
"""


@pytest.mark.parametrize('method', BAD_MAGIC_METHODS)
def test_wrong_magic_used(assert_errors, parse_ast_tree, method):
    """Testing that some magic methods are restricted."""
    tree = parse_ast_tree(magic_method.format(method))

    visiter = WrongClassVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [BadMagicMethodViolation])


@pytest.mark.parametrize('method', [
    '__add__',
    '__init__',
    'next',
    'regular',
])
def test_regular_method_used(assert_errors, parse_ast_tree, method):
    """Testing that other methods are working fine."""
    tree = parse_ast_tree(magic_method.format(method))

    visiter = WrongClassVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])

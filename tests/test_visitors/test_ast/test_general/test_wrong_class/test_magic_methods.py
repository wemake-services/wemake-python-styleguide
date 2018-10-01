# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import BAD_MAGIC_METHODS
from wemake_python_styleguide.violations.best_practices import (
    BadMagicMethodViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

magic_method = """
class Example(object):
    def {0}(): ...
"""


@pytest.mark.parametrize('method', BAD_MAGIC_METHODS)
def test_wrong_magic_used(
    assert_errors, parse_ast_tree, method, default_options,
):
    """Testing that some magic methods are restricted."""
    tree = parse_ast_tree(magic_method.format(method))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BadMagicMethodViolation])


@pytest.mark.parametrize('method', [
    '__add__',
    '__init__',
    'next',
    'regular',
])
def test_regular_method_used(
    assert_errors, parse_ast_tree, method, default_options,
):
    """Testing that other methods are working fine."""
    tree = parse_ast_tree(magic_method.format(method))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

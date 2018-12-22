# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import MAGIC_METHODS_BLACKLIST
from wemake_python_styleguide.violations.best_practices import (
    BadMagicMethodViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

magic_method = """
class Example(object):
    def {0}(self): ...
"""

regular_function = 'def {0}(): ...'


@pytest.mark.parametrize('method', MAGIC_METHODS_BLACKLIST)
def test_wrong_magic_used(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    method,
    mode,
    default_options,
):
    """Testing that some magic methods are restricted."""
    tree = parse_ast_tree(mode(magic_method.format(method)))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BadMagicMethodViolation])
    assert_error_text(visitor, method)


@pytest.mark.parametrize('code', [
    magic_method,
    regular_function,
])
@pytest.mark.parametrize('method', [
    '__add__',
    '__init__',
    'next',
    'regular',
])
def test_regular_method_used(
    assert_errors,
    parse_ast_tree,
    code,
    method,
    mode,
    default_options,
):
    """Testing that other methods are working fine."""
    tree = parse_ast_tree(mode(code.format(method)))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionSubclassViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

class_with_base = """
class Meta({0}):
    '''Docs.'''
"""


@pytest.mark.parametrize('code', [
    class_with_base,
])
def test_base_exception_subclass(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that it is not possible to subclass `BaseException`."""
    tree = parse_ast_tree(class_with_base.format('BaseException'))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BaseExceptionSubclassViolation])

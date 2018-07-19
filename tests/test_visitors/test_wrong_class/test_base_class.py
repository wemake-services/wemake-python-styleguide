# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_class import (
    RequiredBaseClassViolation,
    WrongClassVisitor,
)


def test_wrong_base_class(assert_errors, parse_ast_tree):
    """Testing that not using explicit base class with forbiden."""
    tree = parse_ast_tree("""
    class WithoutBase: ...
    """)

    visiter = WrongClassVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [RequiredBaseClassViolation])


@pytest.mark.parametrize('base', [
    'object',
    'dict',
    'CustomClass',
    'Multiple, Classes, Mixins',
    'Custom, keyword=1',
])
def test_regular_base_classes(assert_errors, parse_ast_tree, base):
    """Testing that regular base classes work."""
    tree = parse_ast_tree("""
    class Example({0}): ...
    """.format(base))

    visiter = WrongClassVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])

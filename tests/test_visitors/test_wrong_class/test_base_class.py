# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_class import (
    RequiredBaseClassViolation,
    WrongClassVisitor,
)


def test_wrong_base_class(assert_errors, parse_ast_tree, default_options):
    """Testing that not using explicit base class is forbiden."""
    tree = parse_ast_tree("""
    class WithoutBase: ...
    """)

    visiter = WrongClassVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [RequiredBaseClassViolation])


def test_wrong_base_class_nested(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that not using explicit base class on nested is forbiden."""
    tree = parse_ast_tree("""
    class Model(object):
        class Meta: ...
    """)

    visiter = WrongClassVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [RequiredBaseClassViolation])


def test_correct_base_class_nested(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that using explicit base class on nested works."""
    tree = parse_ast_tree("""
    class Model(object):
        class Meta(object): ...
    """)

    visiter = WrongClassVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])


@pytest.mark.parametrize('base', [
    'object',
    'dict',
    'CustomClass',
    'Multiple, Classes, Mixins',
    'Custom, keyword=1',
])
def test_regular_base_classes(
    assert_errors, parse_ast_tree, base, default_options,
):
    """Testing that regular base classes work."""
    tree = parse_ast_tree("""
    class Example({0}): ...
    """.format(base))

    visiter = WrongClassVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])

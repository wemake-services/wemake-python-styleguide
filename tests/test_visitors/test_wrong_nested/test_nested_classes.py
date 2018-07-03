# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_nested import (
    NESTED_CLASSES_WHITELIST,
    NestedClassViolation,
    WrongNestedVisitor,
)

nested_class = """
class Parent:
    class {0}: ...
"""

nested_class_in_method = """
class Parent:
    def container(self):
        class {0}: ...
"""

nested_class_in_function = """
def container():
    class {0}: ...
"""


@pytest.mark.parametrize('code', [
    nested_class,
    nested_class_in_method,
    nested_class_in_function,
])
def test_nested_class(assert_errors, parse_ast_tree, code):
    """Testing that nested classes are restricted."""
    tree = parse_ast_tree(code.format('NestedClass'))

    visiter = WrongNestedVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [NestedClassViolation])


@pytest.mark.parametrize('whitelist_name', NESTED_CLASSES_WHITELIST)
@pytest.mark.parametrize('code', [
    nested_class,
])
def test_whitelist_nested_classes(
    assert_errors, parse_ast_tree, whitelist_name, code,
):
    """Testing that it is possible to nest whitelisted classes."""
    tree = parse_ast_tree(code.format(whitelist_name))

    visiter = WrongNestedVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])


@pytest.mark.parametrize('whitelist_name', [
    *NESTED_CLASSES_WHITELIST,
    'NestedClass',
])
@pytest.mark.parametrize('code', [
    nested_class_in_method,
    nested_class_in_function,
])
def test_whitelist_nested_classes_in_functions(
    assert_errors, parse_ast_tree, whitelist_name, code,
):
    """Testing that it is restricted to nest any classes in functions."""
    tree = parse_ast_tree(code.format(whitelist_name))

    visiter = WrongNestedVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [NestedClassViolation])


def test_ordinary_class(assert_errors, parse_ast_tree):
    """Testing that it is possible to write basic classes."""
    tree = parse_ast_tree("""
    class Ordinary:
        def method(self): ...
    """)

    visiter = WrongNestedVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])

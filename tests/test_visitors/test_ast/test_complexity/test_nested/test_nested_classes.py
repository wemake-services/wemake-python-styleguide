# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    NestedClassViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.nested import (
    NESTED_CLASSES_WHITELIST,
    NestedComplexityVisitor,
)

nested_class = """
class Parent(object):
    class {0}(object): ...
"""

nested_class_in_method = """
class Parent(object):
    def container(self):
        class {0}(object): ...
"""

nested_class_in_async_method = """
class Parent(object):
    async def container(self):
        class {0}(object): ...
"""

nested_class_in_function = """
def container():
    class {0}(object): ...
"""

nested_class_in_async_function = """
async def container():
    class {0}(object): ...
"""


@pytest.mark.parametrize('code', [
    nested_class,
    nested_class_in_method,
    nested_class_in_async_method,
    nested_class_in_function,
    nested_class_in_async_function,
])
def test_nested_class(assert_errors, parse_ast_tree, code, default_options):
    """Testing that nested classes are restricted."""
    tree = parse_ast_tree(code.format('NestedClass'))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedClassViolation])


@pytest.mark.parametrize('whitelist_name', NESTED_CLASSES_WHITELIST)
@pytest.mark.parametrize('code', [
    nested_class,
])
def test_whitelist_nested_classes(
    assert_errors, parse_ast_tree, whitelist_name, code, default_options,
):
    """Testing that it is possible to nest whitelisted classes."""
    tree = parse_ast_tree(code.format(whitelist_name))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('whitelist_name', [
    *NESTED_CLASSES_WHITELIST,
    'NestedClass',
])
@pytest.mark.parametrize('code', [
    nested_class_in_method,
    nested_class_in_async_method,
    nested_class_in_function,
    nested_class_in_async_function,
])
def test_whitelist_nested_classes_in_functions(
    assert_errors, parse_ast_tree, whitelist_name, code, default_options,
):
    """Testing that it is restricted to nest any classes in functions."""
    tree = parse_ast_tree(code.format(whitelist_name))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedClassViolation])


def test_ordinary_class(assert_errors, parse_ast_tree, default_options):
    """Testing that it is possible to write basic classes."""
    tree = parse_ast_tree("""
    class Ordinary(object):
        def method(self): ...

    class Second(Ordinary):
        def method(self): ...
    """)

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

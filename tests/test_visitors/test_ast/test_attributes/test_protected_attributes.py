# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.attributes import (
    ProtectedAttributeViolation,
    WrongAttributeVisitor,
)

# Incorrect:

protected_attribute_assigned = 'some._protected = 1'
protected_attribute_accessed = 'print(some._protected)'
protected_method_called = 'some._method()'
protected_method_called_params = 'some._method(12, 33)'

protected_container_attribute = """
class Test(object):
    def __init__(self):
        self.container._print = 1
"""

protected_container_method = """
class Test(object):
    def __init__(self):
        self.container._print()
"""

protected_callable_attribute = """
class Test(object):
    def __init__(self):
        some()._print()
"""

# Correct:

protected_name_definition = '_protected = 1'
protected_name_attr_definition = '_protected.some = 1'
magic_method_called = 'Test.__init__()'
magic_attribute_accessed = 'Test.__dict__'
magic_attribute_definition = 'Test.__dict__ = dict()'

protected_self_attribute = """
class Test(object):
    def __init__(self):
        self._print = 1
"""

protected_self_method = """
class Test(object):
    def __init__(self):
        self._print()
"""

protected_cls_attribute = """
class Test(object):
    @classmethod
    def method(cls):
        cls._print = 'some'
"""

protected_cls_method = """
class Test(object):
    @classmethod
    def method(cls):
        cls._print()
"""

protected_attribute_definition = """
class Test(object):
    _protected = 1
"""

protected_method_definition = """
class Test(object):
    def _protected(self):
        ...
"""

protected_classmethod_definition = """
class Test(object):
    @classmethod
    def _protected(cls):
        ...
"""

protected_super_attribute = """
class Test(object):
    def __init__(self):
        super()._print = 1
"""

protected_super_method = """
class Test(object):
    def __init__(self):
        super()._print()
"""

protected_super_cls_attribute = """
class Test(object):
    @classmethod
    def method(cls):
        super()._print = 'some'
"""

protected_super_cls_method = """
class Test(object):
    @classmethod
    def method(cls):
        super()._print()
"""


@pytest.mark.parametrize('code', [
    protected_attribute_assigned,
    protected_attribute_accessed,
    protected_method_called,
    protected_method_called_params,
    protected_container_attribute,
    protected_container_method,
    protected_callable_attribute,
])
def test_protected_attribute_is_restricted(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Ensures that it is impossible to use protected attributes."""
    tree = parse_ast_tree(code)

    visitor = WrongAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ProtectedAttributeViolation])


@pytest.mark.parametrize('code', [
    protected_name_definition,
    magic_attribute_accessed,
    magic_method_called,
    magic_attribute_definition,
    protected_name_attr_definition,
    protected_self_attribute,
    protected_self_method,
    protected_cls_attribute,
    protected_cls_method,
    protected_attribute_definition,
    protected_method_definition,
    protected_classmethod_definition,
    protected_super_attribute,
    protected_super_method,
    protected_super_cls_attribute,
    protected_super_cls_method,
])
def test_protected_attribute_is_allowed(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Ensures that it is possible to use protected attributes."""
    tree = parse_ast_tree(code)

    visitor = WrongAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.attributes import (
    DirectMagicAttributeAccessViolation,
    WrongAttributeVisitor,
)

# Wrong:

magic_attribute_assigned = 'some.__magic__ = 1'
magic_attribute_accessed = 'print(some.__magic__)'
magic_method_called = 'some.__magic__()'
magic_method_called_params = 'some.__magic__(12, 33)'

magic_container_attribute = """
class Test(object):
    def __init__(self):
        self.container.__magic__ = 1
"""

magic_container_method = """
class Test(object):
    def __init__(self):
        self.container.__magic__()
"""

magic_callable_attribute = """
class Test(object):
    def __init__(self):
        some().__magic__()
"""

# Correct:

magic_allowed_doc = 'print(some.__doc__)'
magic_allowed_name = 'print(some.__name__)'
magic_allowed_qualname = 'print(some.__qualname__)'
magic_allowed_class = 'print(some.__class__)'

magic_name_definition = '__magic__ = 1'
magic_name_attr_definition = '__magic__.some = 1'

magic_self_attribute = """
class Test(object):
    def __init__(self):
        self.__magic__ = 1
"""

magic_self_method = """
class Test(object):
    def __init__(self):
        self.__magic__()
"""

magic_cls_attribute = """
class Test(object):
    @classmethod
    def method(cls):
        cls.__magic__ = 'some'
"""

magic_cls_method = """
class Test(object):
    @classmethod
    def method(cls):
        cls.__magic__()
"""

magic_attribute_definition = """
class Test(object):
    __magic__ = 1
"""

magic_method_definition = """
class Test(object):
    def __magic__(self):
        ...
"""

magic_classmethod_definition = """
class Test(object):
    @classmethod
    def __magic__(cls):
        ...
"""

magic_super_attribute = """
class Test(object):
    def __init__(self):
        super().__magic__ = 1
"""

magic_super_method = """
class Test(object):
    def __init__(self):
        super().__magic__()
"""

magic_super_cls_attribute = """
class Test(object):
    @classmethod
    def method(cls):
        super().__magic__ = 'some'
"""

magic_super_cls_method = """
class Test(object):
    @classmethod
    def method(cls):
        super().__magic__()
"""


@pytest.mark.parametrize('code', [
    magic_attribute_assigned,
    magic_attribute_accessed,
    magic_method_called,
    magic_method_called_params,
    magic_container_attribute,
    magic_container_method,
    magic_callable_attribute,
])
def test_magic_attribute_is_restricted(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that it is impossible to use magic attributes."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [DirectMagicAttributeAccessViolation])
    assert_error_text(visitor, '__magic__')


@pytest.mark.parametrize('code', [
    magic_allowed_doc,
    magic_allowed_name,
    magic_allowed_qualname,
    magic_allowed_class,

    magic_name_definition,
    magic_name_attr_definition,
    magic_self_attribute,
    magic_self_method,
    magic_cls_attribute,
    magic_cls_method,
    magic_attribute_definition,
    magic_method_definition,
    magic_classmethod_definition,
    magic_super_attribute,
    magic_super_method,
    magic_super_cls_attribute,
    magic_super_cls_method,
])
def test_magic_attribute_is_allowed(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that it is possible to use magic attributes."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

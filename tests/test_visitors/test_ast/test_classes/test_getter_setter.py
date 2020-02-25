# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.oop import (
    UnpythonicGetterSetterViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

module_getter_and_setter = """
attribute = 1

def get_attribute():
    ...

def set_attribute():
    ...
"""

static_getter_and_setter = """
attribute = 1

class Test(object):
    @staticmethod
    def get_attribute():
        ...

    @staticmethod
    def set_attribute():
        ...
"""

property_getter_and_setter = """
class Test(object):
    def __init__(self):
        self.attribute = 1

    @property
    def get_attribute(self):
        ...

    @property.setter
    def set_attribute(self):
        ...
"""

child_getter_and_setter = """
class TestParent(object):
    def __init__(self):
        self.attribute = 1

class TestChild(TestParent):
    def get_attribute(self):
        ...

    def set_attribute(self):
        ...
"""

nested_getter_and_setter = """
class Template(object):
    def __init__(self):
        self.attribute = 1

    def some_function(self):
        def get_attribute(self):
            ...
        def set_attribute(self):
            ...
        get_attribute(self)
"""

class_attribute_template = """
class Template(object):
    def __init__(self):
        self.{0} = 1

    {1}
    def {2}(self):
        ...
"""


@pytest.mark.parametrize('code', [
    module_getter_and_setter,
    static_getter_and_setter,
    property_getter_and_setter,
    child_getter_and_setter,
    nested_getter_and_setter,
])
def test_property_getter_and_setter(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that attribute, getter and setter is allowed outside of class."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('first', 'second', 'third'), [
    ('attribute', '', 'get_attribute_some'),
    ('attribute', '', 'some_get_attribute'),
    ('attribute', '', 'get_some_attribute'),
    ('attribute', '', 'attribute_get'),
    ('some_attribute', '', 'get_attribute'),
    ('attribute_some', '', 'get_attribute'),
])
def test_nonmatching_attribute_getter_setter(
    assert_errors,
    parse_ast_tree,
    default_options,
    first,
    second,
    third,
    mode,
):
    """Testing that non matching attribute and getter/setter is allowed."""
    test_instance = class_attribute_template.format(first, second, third)
    tree = parse_ast_tree(mode(test_instance))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('first', 'second', 'third'), [
    ('attribute', '', 'get_attribute'),
    ('_attribute', '', 'get_attribute'),
    ('__attribute', '', 'get_attribute'),
    ('attribute', '@classmethod', 'set_attribute'),
    ('_attribute', '@classmethod', 'set_attribute'),
    ('__attribute', '@classmethod', 'set_attribute'),
])
def test_instance_and_class_getter_setter(
    assert_errors,
    parse_ast_tree,
    default_options,
    first,
    second,
    third,
    mode,
):
    """Testing that instance/class attribute and getter/setter is prohibited."""
    test_instance = class_attribute_template.format(first, second, third)
    tree = parse_ast_tree(mode(test_instance))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnpythonicGetterSetterViolation])

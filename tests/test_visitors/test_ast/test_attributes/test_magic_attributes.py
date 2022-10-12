import pytest

from wemake_python_styleguide.constants import ALL_MAGIC_METHODS
from wemake_python_styleguide.violations.oop import (
    DirectMagicAttributeAccessViolation,
)
from wemake_python_styleguide.visitors.ast.attributes import (
    WrongAttributeVisitor,
)

# Wrong:

magic_attribute_assigned = 'some.{0} = 1'
magic_attribute_accessed = 'print(some.{0})'
magic_method_called = 'some.{0}()'
magic_method_called_params = 'some.{0}(12, 33)'

magic_container_attribute = """
class Test(object):
    def __init__(self):
        self.container.{0} = 1
"""

magic_container_method = """
class Test(object):
    def __init__(self):
        self.container.{0}()
"""

magic_callable_attribute = """
class Test(object):
    def __init__(self):
        some().{0}()
"""

# Correct:

magic_name_definition = '{0} = 1'
magic_name_attr_definition = '{0}.some = 1'

magic_self_attribute = """
class Test(object):
    def __init__(self):
        self.{0} = 1
"""

magic_self_method = """
class Test(object):
    def __init__(self):
        self.{0}()
"""

magic_cls_attribute = """
class Test(object):
    @classmethod
    def method(cls):
        cls.{0} = 'some'
"""

magic_cls_method = """
class Test(object):
    @classmethod
    def method(cls):
        cls.{0}()
"""

magic_attribute_definition = """
class Test(object):
    {0} = 1
"""

magic_method_definition = """
class Test(object):
    def {0}(self):
        ...
"""

magic_classmethod_definition = """
class Test(object):
    @classmethod
    def {0}(cls):
        ...
"""

magic_super_attribute = """
class Test(object):
    def __init__(self):
        super().{0} = 1
"""

magic_super_method = """
class Test(object):
    def __init__(self):
        super().{0}()
"""

magic_super_cls_attribute = """
class Test(object):
    @classmethod
    def method(cls):
        super().{0} = 'some'
"""

magic_super_cls_method = """
class Test(object):
    @classmethod
    def method(cls):
        super().{0}()
"""

magic_wrapper_method = """
class Test(object):

    def {0}(cls):
        self.conn.{0}()
"""

magic_wrapper_method_inside_stacked_cls = """
class StackedTest(object):

    def something(cls):
        class Test(object):
            def {0}(cls):
                self.conn.{0}()

        anything()
"""


@pytest.mark.parametrize('attribute', [
    '__truediv__',
    '__radd__',
    '__iter__',
    '__int__',
    '__float__',
    '__repr__',
    '__coerce__',
    '__str__',
    '__next__',
])
@pytest.mark.parametrize('code', [
    magic_attribute_assigned,
    magic_attribute_accessed,
    magic_method_called,
    magic_method_called_params,
    magic_container_attribute,
    magic_container_method,
    magic_callable_attribute,
])
def test_disallowed_magic_attribute_is_restricted(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    attribute,
    default_options,
    mode,
):
    """Ensures that it is impossible to use certain magic attributes."""
    tree = parse_ast_tree(mode(code.format(attribute)))

    visitor = WrongAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [DirectMagicAttributeAccessViolation])
    assert_error_text(visitor, attribute)


@pytest.mark.parametrize('attribute', [
    '__magic__',
    '__str__',
    '__float__',
    '__members__',
    '__path__',
    '__foo__',
    '__unknown__',
])
@pytest.mark.parametrize('code', [
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
def test_magic_attribute_correct_contexts(
    assert_errors,
    parse_ast_tree,
    code,
    attribute,
    default_options,
    mode,
):
    """Ensures it is possible to use magic attributes in certain contexts."""
    tree = parse_ast_tree(mode(code.format(attribute)))

    visitor = WrongAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('attribute', [
    'regular',
    '__doc__',
    '__name__',
    '__class__',
    '__qualname__',
    '__subclasses__',
    '__mro__',
    '__version__',
    '__path__',
    '__bases__',
    '__members__',
    '__unknown__',
    '__foo__',
])
@pytest.mark.parametrize('code', [
    magic_attribute_assigned,
    magic_attribute_accessed,
    magic_method_called,
    magic_method_called_params,
    magic_container_attribute,
    magic_container_method,
    magic_callable_attribute,
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
def test_other_magic_attributes_allowed(
    assert_errors,
    parse_ast_tree,
    code,
    attribute,
    default_options,
    mode,
):
    """
    Tests if regular attributes are allowed.

    Ensures that it is possible to use regular attributes, as well as
    magic attributes for which no (known) alternative exists.
    """
    tree = parse_ast_tree(mode(code.format(attribute)))

    visitor = WrongAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('attribute', ALL_MAGIC_METHODS)
@pytest.mark.parametrize('code', [
    magic_wrapper_method,
    magic_wrapper_method_inside_stacked_cls,
])
def test_happy_little_magic_wrapper_methods(
    assert_errors,
    parse_ast_tree,
    code,
    attribute,
    default_options,
    mode,
):
    """
    Test calling magic methods with the same name.

    Ensure that calling magic method inside magic method with the same
    name does not trigger any violations.
    """
    tree = parse_ast_tree(mode(code.format(attribute)))

    visitor = WrongAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

import pytest

from wemake_python_styleguide.visitors.ast.attributes import (
    ProtectedAttributeViolation,
    WrongAttributeVisitor,
)

# Wrong:

protected_attribute_assigned = 'some._protected = 1'
protected_attribute_accessed = 'print(some._protected)'
protected_method_called = 'some._protected()'
protected_method_called_params = 'some._protected(12, 33)'
builtin_protected_call = 'True()._protected = 1'  # to make coverage happy

protected_container_attribute = """
class Test(object):
    def __init__(self):
        self.container._protected = 1
"""

protected_container_method = """
class Test(object):
    def __init__(self):
        self.container._protected()
"""

protected_callable_attribute = """
class Test(object):
    def __init__(self):
        some()._protected()
"""

# Correct:

protected_name_definition = '_protected = 1'
protected_name_attr_definition = '_protected.some = 1'

protected_self_attribute = """
class Test(object):
    def __init__(self):
        self._protected = 1
"""

protected_self_method = """
class Test(object):
    def __init__(self):
        self._protected()
"""

protected_cls_attribute = """
class Test(object):
    @classmethod
    def method(cls):
        cls._protected = 'some'
"""

protected_cls_method = """
class Test(object):
    @classmethod
    def method(cls):
        cls._protected()
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
        super()._protected = 1
"""

protected_super_method = """
class Test(object):
    def __init__(self):
        super()._protected()
"""

protected_super_cls_attribute = """
class Test(object):
    @classmethod
    def method(cls):
        super()._protected = 'some'
"""

protected_super_cls_method = """
class Test(object):
    @classmethod
    def method(cls):
        super()._protected()
"""


@pytest.mark.filterwarnings('ignore::SyntaxWarning')
@pytest.mark.parametrize('code', [
    protected_attribute_assigned,
    protected_attribute_accessed,
    builtin_protected_call,
    protected_method_called,
    protected_method_called_params,
    protected_container_attribute,
    protected_container_method,
    protected_callable_attribute,
])
def test_protected_attribute_is_restricted(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that it is impossible to use protected attributes."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ProtectedAttributeViolation])
    assert_error_text(visitor, '_protected')


@pytest.mark.parametrize('code', [
    protected_name_definition,
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
    mode,
):
    """Ensures that it is possible to use protected attributes."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

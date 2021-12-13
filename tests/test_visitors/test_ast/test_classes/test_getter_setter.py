import pytest

from wemake_python_styleguide.violations.oop import (
    UnpythonicGetterSetterViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassBodyVisitor

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

paired_getter_and_setter = """
class Test(object):
    def get_attribute():
        ...

    def set_attribute():
        ...
"""

property_getter_and_setter = """
class Test(object):
    def __init__(self):
        self.attribute = 1

    @property
    def attribute(self):
        ...

    @attribute.setter
    def attribute(self):
        ...
"""

dataclass_property_getter_setter = """
@dataclass
class DataClass(object):
    attribute: int

    @property
    def attribute(self):
        ...

    @attribute.setter
    def attribute(self):
        ...
"""

dataclass_incorrect_property_getter_setter = """
@dataclass
class DataClass(object):
    attribute: int

    @property
    def get_attribute(self):
        ...

    @attribute.setter
    def set_attribute(self):
        ...
"""

dataclass_getter_setter = """
@dataclass
class DataClass(object):
    attribute: int

    def get_attribute(self):
        ...

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

class_getter_and_setter_attributes = """
class Test(object):
    attribute = 1
    get_attribute = 1
    set_attribute = 1
"""

instance_getter_and_setter_attributes = """
class Test(object):
    def __init__(self):
        self.attribute = 1
        self.get_attribute = 1
        self.set_attribute = 1
"""

other_getter_and_setter = """
class Test(object):
    def __init__(self, other):
        other.attr = self.some()

    def get_attr(self):
        return something.unrelated()
"""

instance_attribute_template = """
class Template(object):
    def __init__(self):
        self.{0}{1}{2}

    {3}
    def {4}(self):
        ...
"""

class_attribute_template = """
class Template(object):
    {0}{1}{2}

    {3}
    def {4}:
        ...
"""

class_mixed = """
class Test(object):
    first: int
    second = 2
    third: int = 3

    def __init__(self):
        self.{0}{1} = 5

    def get_{2}(self):
        ...

    def set_{3}(self):
        ...
"""


@pytest.mark.parametrize('code', [
    module_getter_and_setter,
    nested_getter_and_setter,
    property_getter_and_setter,
    class_getter_and_setter_attributes,
    instance_getter_and_setter_attributes,
    dataclass_property_getter_setter,
    other_getter_and_setter,
])
def test_valid_getter_and_setter(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that correct usage of getter/setter is allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongClassBodyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    dataclass_getter_setter,
    dataclass_incorrect_property_getter_setter,
    static_getter_and_setter,
    child_getter_and_setter,
    paired_getter_and_setter,
])
def test_invalid_getter_and_setter(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that wrong use of getter/setter is prohibited."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongClassBodyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        UnpythonicGetterSetterViolation,
        UnpythonicGetterSetterViolation,
    ])


@pytest.mark.parametrize('access', [''])
@pytest.mark.parametrize('assignment', [' = 1'])
@pytest.mark.parametrize(('attribute_name', 'annotation', 'method_name'), [
    ('attribute', '', 'get_attribute_some'),
    ('attribute', '', 'some_get_attribute'),
    ('attribute', '', 'get_some_attribute'),
    ('attribute', '', 'attribute_get'),
    ('some_attribute', '', 'get_attribute'),
    ('attribute_some', '', 'get_attribute'),
])
def test_nonmatching_instance(
    assert_errors,
    parse_ast_tree,
    default_options,
    access,
    assignment,
    attribute_name,
    annotation,
    method_name,
    mode,
):
    """Testing that non matching attribute and getter/setter is allowed."""
    test_instance = instance_attribute_template.format(
        access, attribute_name, assignment, annotation, method_name,
    )
    tree = parse_ast_tree(mode(test_instance))

    visitor = WrongClassBodyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('access', ['', '_', '__'])
@pytest.mark.parametrize('assignment', [
    ' = 1',
    ': int = 1',
    ' = self.other = 1',
    ', self.other = 1, 2',
])
@pytest.mark.parametrize(('attribute_name', 'annotation', 'method_name'), [
    ('attribute', '', 'get_attribute'),
    ('attribute', '', 'set_attribute'),
    ('attribute_some', '', 'get_attribute_some'),
    ('some_attribute', '', 'set_some_attribute'),
    ('attribute', '@classmethod', 'get_attribute'),
    ('attribute', '@classmethod', 'set_attribute'),
    ('attribute', '@staticmethod', 'get_attribute'),
    ('attribute', '@staticmethod', 'set_attribute'),
    ('attribute', '@property', 'get_attribute'),
    ('attribute', '@attribute.setter', 'set_attribute'),
])
def test_instance_getter_setter(
    assert_errors,
    parse_ast_tree,
    default_options,
    access,
    assignment,
    attribute_name,
    annotation,
    method_name,
    mode,
):
    """Testing that instance attribute and getter/setter is prohibited."""
    test_instance = instance_attribute_template.format(
        access, attribute_name, assignment, annotation, method_name,
    )
    tree = parse_ast_tree(mode(test_instance))

    visitor = WrongClassBodyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnpythonicGetterSetterViolation])


@pytest.mark.parametrize('access', [''])
@pytest.mark.parametrize('assignment', [' = 1'])
@pytest.mark.parametrize(('attribute_name', 'annotation', 'method_name'), [
    ('attribute', '@classmethod', 'get_attribute_some(self)'),
    ('attribute', '@classmethod', 'some_get_attribute(self)'),
    ('attribute', '@classmethod', 'get_some_attribute(self)'),
    ('attribute', '@classmethod', 'attribute_get(self)'),
    ('some_attribute', '@classmethod', 'get_attribute(self)'),
    ('attribute_some', '@classmethod', 'get_attribute(self)'),
])
def test_nonmatching_class(
    assert_errors,
    parse_ast_tree,
    default_options,
    access,
    attribute_name,
    annotation,
    method_name,
    assignment,
    mode,
):
    """Testing that non matching attribute and getter/setter is allowed."""
    test_instance = class_attribute_template.format(
        access, attribute_name, assignment, annotation, method_name,
    )
    tree = parse_ast_tree(mode(test_instance))

    visitor = WrongClassBodyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('access', ['', '_', '__'])
@pytest.mark.parametrize('assignment', [
    ' = 1',
    ': int = 1',
    ': int',
    ' = other = 1',
    ', other = 1, 2',
])
@pytest.mark.parametrize(('attribute_name', 'annotation', 'method_name'), [
    ('attribute', '@classmethod', 'get_attribute(cls)'),
    ('attribute', '@classmethod', 'set_attribute(cls)'),
    ('attribute_some', '@classmethod', 'get_attribute_some(self)'),
    ('some_attribute', '@classmethod', 'set_some_attribute(self)'),
    ('attribute', '', 'get_attribute(cls)'),
    ('attribute', '', 'set_attribute(cls)'),
    ('attribute', '@staticmethod', 'get_attribute(cls)'),
    ('attribute', '@staticmethod', 'set_attribute(cls)'),
])
def test_class_attributes_getter_setter(
    assert_errors,
    parse_ast_tree,
    default_options,
    attribute_name,
    access,
    annotation,
    method_name,
    assignment,
    mode,
):
    """Testing that using getter/setters with class attributes is prohibited."""
    test_instance = class_attribute_template.format(
        access, attribute_name, assignment, annotation, method_name,
    )
    tree = parse_ast_tree(mode(test_instance))

    visitor = WrongClassBodyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnpythonicGetterSetterViolation])


@pytest.mark.parametrize('access', ['', '_', '__'])
@pytest.mark.parametrize(('first', 'second', 'third'), [
    ('attribute', 'some', 'other'),
    ('attribute', 'some', 'another'),
])
def test_class_mixed(
    assert_errors,
    parse_ast_tree,
    default_options,
    access,
    first,
    second,
    third,
    mode,
):
    """Testing correct use of methods with get/set in name."""
    test_instance = class_mixed.format(access, first, second, third)
    tree = parse_ast_tree(mode(test_instance))

    visitor = WrongClassBodyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

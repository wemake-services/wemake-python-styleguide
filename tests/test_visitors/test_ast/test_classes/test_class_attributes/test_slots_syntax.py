# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.oop import WrongSlotsViolation
from wemake_python_styleguide.visitors.ast.classes import WrongSlotsVisitor

class_body_template = """
class ClassWithSlots(object):
    __slots__ = {0}
"""

class_body_typed_template = """
class ClassWithSlots(object):
    __slots__: tuple = {0}
"""

not_a_slot = """
class ClassWithoutSlots(object):
    some_other = {0}
"""

wrong_slots = (
    '[]',
    '["field", "other"]',
    '[x for x in some()]',
    '("",)',
    '(x for x in some())',
    '("a", "a")',  # duplicate
    '(1,)',
    '(variable,)',
    '{"name"}',
    '{elem for elem in some_set()}',
    '{1, 2}',
    '("just string")',
    '"string"',
    '1',
    '1.2',
    '-1',
    'None',
    'False',
    'SomeOther.__slots__ + ("child",)',
    'SomeOther.__slots__ + {"child"}',
    '(*some, *some)',
    '(*some.attr, *some.attr)',
    '(*call(), *call())',
    '("123",)',
    '("1_var",)',
    '("*notvalid",)',
    '("*a", *a)',
)

correct_slots = (
    '()',
    '("A",)',
    '("a", "b1")',
    '("a", *other)',
    '("a", *a)',
    '(*Test.Parent, "field")',
    '(*first, *second)',
    'SomeOther.__slots__',
    'some_call()',
    'some.attr',
    'some.method()',
    'some.method().attr',
    'Class.method(10, 10, "a")',
    'some[ast]',
    'some.attr[0].method()',
    'some[0].attr',
)


@pytest.mark.parametrize('template', [
    class_body_template,
    class_body_typed_template,
])
@pytest.mark.parametrize('code', wrong_slots)
def test_incorrect_slots(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    template,
):
    """Testing that incorrect slots are prohibited."""
    tree = parse_ast_tree(template.format(code))

    visitor = WrongSlotsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongSlotsViolation])


@pytest.mark.parametrize('template', [
    class_body_template,
    class_body_typed_template,
])
@pytest.mark.parametrize('code', correct_slots)
def test_correct_slots(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    template,
):
    """Testing that correct slots are allowed."""
    tree = parse_ast_tree(template.format(code))

    visitor = WrongSlotsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    not_a_slot,
])
@pytest.mark.parametrize('code', wrong_slots + correct_slots)
def test_not_slots(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    template,
):
    """Testing that not slots are correct."""
    tree = parse_ast_tree(template.format(code))

    visitor = WrongSlotsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

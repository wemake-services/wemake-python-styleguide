# -*- coding: utf-8 -*-

import string

import pytest

from wemake_python_styleguide.violations.naming import (
    PrivateNameViolation,
    TooShortVariableNameViolation,
    UpperCaseAttributeViolation,
    WrongVariableNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming import (
    VARIABLE_NAMES_BLACKLIST,
    WrongNameVisitor,
)

static_attribute = """
class Test:
    {0} = None
"""

instance_attribute = """
class Test:
    def __init__(self):
        self.{0} = 123
"""


@pytest.mark.parametrize('bad_name', VARIABLE_NAMES_BLACKLIST)
@pytest.mark.parametrize('code', [
    static_attribute,
    instance_attribute,
])
def test_wrong_attributes_names(
    assert_errors, parse_ast_tree, bad_name, code, default_options,
):
    """Testing that attribute can not have blacklisted names."""
    tree = parse_ast_tree(code.format(bad_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongVariableNameViolation])


@pytest.mark.parametrize('short_name', string.ascii_letters)
@pytest.mark.parametrize('code', [
    static_attribute,
    instance_attribute,
])
def test_too_short_attribute_names(
    assert_errors, parse_ast_tree, short_name, code, default_options,
):
    """Testing that attribute can not have too short names."""
    tree = parse_ast_tree(code.format(short_name.lower()))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooShortVariableNameViolation])


@pytest.mark.parametrize('code', [
    static_attribute,
    instance_attribute,
])
def test_private_attribute_names(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that attribute can not have private names."""
    tree = parse_ast_tree(code.format('__private_name'))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [PrivateNameViolation])


@pytest.mark.parametrize('correct_name', [
    'correct_name',
    'xy',
    'test1',
    '_protected',
    '__magic__',
])
@pytest.mark.parametrize('code', [
    static_attribute,
    instance_attribute,
])
def test_correct_attribute_name(
    assert_errors, parse_ast_tree, code, correct_name, default_options,
):
    """Testing that attribute can have normal names."""
    tree = parse_ast_tree(code.format(correct_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('non_snake_case_name', [
    'Abc',
    'A_CONSTANT',
    'AAA',
    'CONST1_bc',
    'camelCase',
    '_A_c',
])
def test_upper_case_class_attributes(
    assert_errors, parse_ast_tree, non_snake_case_name, default_options,
):
    """Testing that attribute can not have too short names."""
    tree = parse_ast_tree(static_attribute.format(non_snake_case_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UpperCaseAttributeViolation])


@pytest.mark.parametrize('snake_case_name', [
    'abc',
    'a_variable',
    'aaa',
    'two_minutes_to_midnight',
    'variable_42',
    '_a_c',
])
def test_snake_case_class_attributes(
    assert_errors, parse_ast_tree, snake_case_name, default_options,
):
    """Testing that attribute can not have too short names."""
    tree = parse_ast_tree(static_attribute.format(snake_case_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

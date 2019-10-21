# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.oop import (
    WrongSuperCallAccessViolation,
    WrongSuperCallViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallVisitor,
)

# Template for super call with method and property tests

super_call_with_access = """
class Example(Parent):
    def some_thing(self):
        super({0}).{1}
"""

# Correct:

correct_super_call = """
class Example(object):
    def some_method(self, arg1):
        super().some_method(arg1)
"""

# There are no violations in this example.
# See: https://github.com/wemake-services/wemake-python-styleguide/issues/520
correct_regression520 = """
class Test:
    def __init__(self):
        super().__init__()


def another():
    def func():
        return 1

    return func
"""

# Wrong:

super_call_in_module = """
super()
"""

super_call_in_module_with_arguments = """
super(SomeClass, instance)
"""

super_call_in_function = """
def some_function():
    super()
"""

super_call_in_function_with_arguments = """
def some_function():
    super(SomeClass, instance)
"""

super_call_in_method_with_arguments = """
class Example(object):
    def some_method(self, arg1):
        super(Example, self).some_method(arg1)
"""


@pytest.mark.parametrize('code', [
    correct_super_call,
    correct_regression520,
])
def test_correct_super_call(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that calling `super` in method is fine."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    super_call_in_module,
    super_call_in_function,
    super_call_in_method_with_arguments,
])
def test_wrong_super_call(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that calling `super` has limitations."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongSuperCallViolation])


@pytest.mark.parametrize('code', [
    super_call_in_function_with_arguments,
    super_call_in_module_with_arguments,
])
def test_double_wrong_super_call(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that it is possible to have two violations with `super`."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        WrongSuperCallViolation,
        WrongSuperCallViolation,
    ])


@pytest.mark.parametrize('code', [
    super_call_with_access,
])
@pytest.mark.parametrize(('arg', 'prop'), [
    ('', 'other()'),
    ('', 'other'),
    ('', 'other.nested'),
    ('', 'other.method()'),
    ('', 'other["key"]'),
])
def test_wrong_access_super_call_with_no_args(
    assert_errors,
    parse_ast_tree,
    code,
    arg,
    prop,
    default_options,
    mode,
):
    """Testing that calling `super` with incorrect access is restricted."""
    tree = parse_ast_tree(mode(code.format(arg, prop)))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        WrongSuperCallAccessViolation,
    ])


@pytest.mark.parametrize('code', [
    super_call_with_access,
])
@pytest.mark.parametrize(('arg', 'prop'), [
    ('Class, self', 'other()'),
    ('Class, self', 'other'),
    ('Class, self', 'other.nested'),
    ('Class, self', 'other.method()'),
    ('Class, self', 'other["key"]'),
])
def test_wrong_access_super_call_with_args(
    assert_errors,
    parse_ast_tree,
    code,
    arg,
    prop,
    default_options,
    mode,
):
    """Testing that calling `super` with incorrect access is restricted."""
    tree = parse_ast_tree(mode(code.format(arg, prop)))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        WrongSuperCallAccessViolation,
        WrongSuperCallViolation,
    ])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.oop import WrongSuperCallViolation
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallVisitor,
)

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

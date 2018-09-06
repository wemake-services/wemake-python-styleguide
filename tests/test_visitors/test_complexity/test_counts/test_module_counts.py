# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.complexity.counts import (
    ModuleMembersVisitor,
    TooManyModuleMembersViolation,
)

module_with_function_and_class = """
def first(): ...

class Second(object): ...
"""

module_with_methods = """
class First(object):
    def method(self): ...

class Second(object):
    def method2(self): ...
"""


@pytest.mark.parametrize('code', [
    module_with_function_and_class,
    module_with_methods,
])
def test_module_counts_normal(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that classes and functions in a module work well."""
    tree = parse_ast_tree(code)

    visiter = ModuleMembersVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])


@pytest.mark.parametrize('code', [
    module_with_function_and_class,
    module_with_methods,
])
def test_module_counts_violation(
    assert_errors, parse_ast_tree, code, options,
):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    option_values = options(max_module_members=1)
    visiter = ModuleMembersVisitor(option_values)
    visiter.visit(tree)

    assert_errors(visiter, [TooManyModuleMembersViolation])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.counts import (
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

    visitor = ModuleMembersVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


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
    visitor = ModuleMembersVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyModuleMembersViolation])

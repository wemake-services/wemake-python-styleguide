# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.counts import (
    MethodMembersVisitor,
    TooManyMethodsViolation,
)

module_without_methods = """
def first(): ...

def second(): ...
"""

class_with_methods = """
class First(object):
    def method(self): ...

    def method2(self): ...
"""

class_with_class_methods = """
class First(object):
    @classmethod
    def method(cls): ...

    @classmethod
    def method2(cls): ...
"""


@pytest.mark.parametrize('code', [
    module_without_methods,
    class_with_methods,
    class_with_class_methods,
])
def test_method_counts_normal(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that regular classes and functions work well."""
    tree = parse_ast_tree(code)

    visitor = MethodMembersVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    class_with_methods,
    class_with_class_methods,
])
def test_method_counts_violation(
    assert_errors, parse_ast_tree, code, options,
):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    option_values = options(max_methods=1)
    visitor = MethodMembersVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyMethodsViolation])

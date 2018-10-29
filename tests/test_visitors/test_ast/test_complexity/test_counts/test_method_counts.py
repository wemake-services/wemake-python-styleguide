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

module_without_methods_with_async_functions = """
async def first(): ...

async def second(): ...
"""

module_without_methods_with_async_and_usual_functions = """
def first(): ...

async def second(): ...
"""

class_with_methods = """
class First(object):
    def method(self): ...

    def method2(self): ...
"""

class_with_async_methods = """
class First(object):
    async def method(self): ...

    async def method2(self): ...
"""

class_with_async_and_usual_methods = """
class First(object):
    def method(self): ...

    async def method2(self): ...
"""

class_with_class_methods = """
class First(object):
    @classmethod
    def method(cls): ...

    @classmethod
    def method2(cls): ...
"""

class_with_async_class_methods = """
class First(object):
    @classmethod
    async def method(cls): ...

    @classmethod
    async def method2(cls): ...
"""

class_with_async_and_usual_class_methods = """
class First(object):
    @classmethod
    def method(cls): ...

    @classmethod
    async def method2(cls): ...
"""


@pytest.mark.parametrize('code', [
    module_without_methods,
    module_without_methods_with_async_functions,
    module_without_methods_with_async_and_usual_functions,
    class_with_methods,
    class_with_async_methods,
    class_with_async_and_usual_methods,
    class_with_class_methods,
    class_with_async_class_methods,
    class_with_async_and_usual_class_methods,
])
def test_method_counts_normal(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that regular classes and functions work well."""
    tree = parse_ast_tree(code)

    visitor = MethodMembersVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    class_with_methods,
    class_with_async_methods,
    class_with_async_and_usual_methods,
    class_with_class_methods,
    class_with_async_class_methods,
    class_with_async_and_usual_class_methods,
])
def test_method_counts_violation(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    options,
):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    option_values = options(max_methods=1)
    visitor = MethodMembersVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyMethodsViolation])
    assert_error_text(visitor, '2')

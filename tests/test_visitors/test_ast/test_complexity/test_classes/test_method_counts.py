import pytest

from wemake_python_styleguide.visitors.ast.complexity.classes import (
    MethodMembersVisitor,
    TooManyMethodsViolation,
)

module_without_methods = """
def first(): ...

def second(): ...
"""

module_with_async_functions = """
async def first(): ...

async def second(): ...
"""

module_async_and_usual_functions = """
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

class_with_staticmethods = """
class First(object):
    @staticmethod
    def method(cls): ...

    @staticmethod
    def method2(cls): ...
"""

class_with_async_staticmethods = """
class First(object):
    @staticmethod
    async def method(cls): ...

    @staticmethod
    async def method2(cls): ...
"""

# regression1779

class_with_overloades = """
class First(object):
    @overload
    def my_method(self): ...

    @typing.overload
    def my_method(self): ...
"""


@pytest.mark.parametrize('code', [
    module_without_methods,
    module_with_async_functions,
    module_async_and_usual_functions,
    class_with_methods,
    class_with_async_methods,
    class_with_async_and_usual_methods,
    class_with_class_methods,
    class_with_async_class_methods,
    class_with_async_and_usual_class_methods,
    class_with_staticmethods,
    class_with_async_staticmethods,
    class_with_overloades,
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
    class_with_staticmethods,
    class_with_async_staticmethods,
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
    assert_error_text(visitor, '2', option_values.max_methods)


@pytest.mark.parametrize('code', [
    class_with_overloades,
])
def test_method_counts_exceptions(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Testing that violations are raised not when using special cases."""
    tree = parse_ast_tree(code)

    option_values = options(max_methods=0)
    visitor = MethodMembersVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

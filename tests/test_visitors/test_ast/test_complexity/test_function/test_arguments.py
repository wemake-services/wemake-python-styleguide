# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
    TooManyArgumentsViolation,
)

function_without_arguments = 'def function(): ...'
function_with_single_argument = 'def function(arg1): ...'
function_with_single_args = 'def function(*args): ...'
function_with_single_kwargs = 'def function(**kwargs): ...'
function_with_single_kwonly = 'def function(*, kwonly=True): ...'

method_without_arguments = """
class Test(object):
    def method(self): ...
"""

method_with_single_argument = """
class Test(object):
    def method(self, arg1): ...
"""

method_with_single_args = """
class Test(object):
    def method(self, *args): ...
"""

method_with_single_kwargs = """
class Test(object):
    def method(self, **kwargs): ...
"""

method_with_single_kwonly = """
class Test(object):
    def method(self, *, kwonly=True): ...
"""

classmethod_without_arguments = """
class Test(object):
    @classmethod
    def method(cls): ...
"""

classmethod_with_single_argument = """
class Test(object):
    @classmethod
    def method(cls, arg1): ...
"""

classmethod_with_single_args = """
class Test(object):
    @classmethod
    def method(cls, *args): ...
"""

classmethod_with_single_kwargs = """
class Test(object):
    @classmethod
    def method(cls, **kwargs): ...
"""

classmethod_with_single_kwonly = """
class Test(object):
    @classmethod
    def method(cls, *, kwonly=True): ...
"""

new_method_without_arguments = """
class Test(object):
    def __new__(cls): ...
"""

new_method_single_argument = """
class Test(object):
    def __new__(cls, arg1): ...
"""

metaclass_without_arguments = """
class TestMeta(type):
    def method(cls): ...
"""

metaclass_with_single_argument = """
class TestMeta(type):
    def method(cls, arg1): ...
"""


@pytest.mark.parametrize('code', [
    function_without_arguments,
    function_with_single_argument,
    function_with_single_args,
    function_with_single_kwargs,
    function_with_single_kwonly,
    method_without_arguments,
    method_with_single_argument,
    method_with_single_args,
    method_with_single_kwargs,
    method_with_single_kwonly,
    classmethod_without_arguments,
    classmethod_with_single_argument,
    classmethod_with_single_args,
    classmethod_with_single_kwargs,
    classmethod_with_single_kwonly,
    new_method_without_arguments,
    new_method_single_argument,
    metaclass_without_arguments,
    metaclass_with_single_argument,
])
def test_correct_arguments_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Ensures that functions with correct argument count works."""
    tree = parse_ast_tree(code)

    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_without_arguments,
    function_with_single_argument,
    function_with_single_args,
    function_with_single_kwargs,
    function_with_single_kwonly,
    method_without_arguments,
    method_with_single_argument,
    method_with_single_args,
    method_with_single_kwargs,
    method_with_single_kwonly,
    classmethod_without_arguments,
    classmethod_with_single_argument,
    classmethod_with_single_args,
    classmethod_with_single_kwargs,
    classmethod_with_single_kwonly,
    new_method_without_arguments,
    new_method_single_argument,
    metaclass_without_arguments,
    metaclass_with_single_argument,
])
def test_single_argument_count(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Ensures that functions with correct argument count works."""
    tree = parse_ast_tree(code)

    option_values = options(max_arguments=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_with_single_argument,
    function_with_single_args,
    function_with_single_kwargs,
    function_with_single_kwonly,
    method_with_single_argument,
    method_with_single_args,
    method_with_single_kwargs,
    method_with_single_kwonly,
    classmethod_with_single_argument,
    classmethod_with_single_args,
    classmethod_with_single_kwargs,
    classmethod_with_single_kwonly,
    new_method_single_argument,
    metaclass_with_single_argument,
])
def test_single_argument_count_valid(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Ensures that functions raise violation when there are multiple args."""
    tree = parse_ast_tree(code)

    option_values = options(max_arguments=0)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyArgumentsViolation])


@pytest.mark.parametrize('code', [
    function_without_arguments,
    method_without_arguments,
    classmethod_without_arguments,
    new_method_without_arguments,
    metaclass_without_arguments,
])
def test_no_arguments(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Ensures that functions with no arguments work."""
    tree = parse_ast_tree(code)

    option_values = options(max_arguments=0)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

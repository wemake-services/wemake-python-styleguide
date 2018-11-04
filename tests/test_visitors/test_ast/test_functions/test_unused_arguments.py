# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    UnusedArgumentIsUsedViolation,
    UnusedArgumentViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionDefinitionVisitor,
)

regular_function_argument = """
def proxy({0}):
    {1}
"""

regular_function_default = """
def proxy({0}=5):
    {1}
"""

regular_function_args = """
def proxy(*{0}):
    {1}
"""

regular_function_kwargs = """
def proxy(**{0}):
    {1}
"""

regular_function_kwonly = """
def proxy(*, {0}):
    {1}
"""

regular_function_kwonly_default = """
def proxy(*, {0}=None):
    {1}
"""

regular_method_argument = """
class Test(object):
    def proxy(self, {0}):
        {1}
"""

regular_method_default = """
class Test(object):
    @classmethod
    def proxy(cls, {0}=5):
        {1}
"""

regular_method_args = """
class Test(type):
    def __new__(mcs, *{0}):
        {1}
"""

regular_method_kwargs = """
class Test(object):
    def proxy(self, **{0}):
        {1}
"""

regular_method_kwonly = """
class Test(object):
    def proxy(self, *, {0}):
        {1}
"""

regular_method_kwonly_default = """
class Test(object):
    def proxy(self, *, {0}=None):
        {1}
"""


@pytest.mark.parametrize('argument', [
    'arg',
    'class_',
    'klass',
    'some_value',
])
@pytest.mark.parametrize('body', [
    'nested = {0} + 1',
    '{0} = {0} + 5',
    'print({0})',
    '{0}.attribute',
    '{0}.method()',
    'assert {0}',
    'return {0}',
])
@pytest.mark.parametrize('code', [
    regular_function_argument,
    regular_function_default,
    regular_function_args,
    regular_function_kwargs,
    regular_function_kwonly,
    regular_function_kwonly_default,
    regular_method_argument,
    regular_method_default,
    regular_method_args,
    regular_method_kwargs,
    regular_method_kwonly,
    regular_method_kwonly_default,
])
def test_regular_arguments_used(
    assert_errors,
    parse_ast_tree,
    argument,
    body,
    code,
    default_options,
    mode,
):
    """Testing that regular arguments are fine."""
    function_body = body.format(argument)
    tree = parse_ast_tree(mode(code.format(argument, function_body)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('argument', [
    'arg',
    'class_',
    'klass',
    'some_value',
])
@pytest.mark.parametrize('code', [
    regular_function_argument,
    regular_function_default,
    regular_function_args,
    regular_function_kwargs,
    regular_function_kwonly,
    regular_function_kwonly_default,
    regular_method_argument,
    regular_method_default,
    regular_method_args,
    regular_method_kwargs,
    regular_method_kwonly,
    regular_method_kwonly_default,
])
def test_regular_arguments_unused_override(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    argument,
    code,
    default_options,
    mode,
):
    """Testing that regular arguments are fine."""
    function_body = '{0} = 1'.format(argument)
    tree = parse_ast_tree(mode(code.format(argument, function_body)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedArgumentViolation])
    assert_error_text(visitor, argument)


@pytest.mark.parametrize('argument', [
    'arg',
    'class_',
    'klass',
    'some_value',
])
@pytest.mark.parametrize('code', [
    regular_function_argument,
    regular_function_default,
    regular_function_args,
    regular_function_kwargs,
    regular_function_kwonly,
    regular_function_kwonly_default,
    regular_method_argument,
    regular_method_default,
    regular_method_args,
    regular_method_kwargs,
    regular_method_kwonly,
    regular_method_kwonly_default,
])
def test_regular_arguments_unused(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    argument,
    code,
    default_options,
    mode,
):
    """Testing that unused arguments are restricted."""
    tree = parse_ast_tree(mode(code.format(argument, '...')))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedArgumentViolation])
    assert_error_text(visitor, argument)


@pytest.mark.parametrize('argument', [
    '_arg',
    '_klass',
    '_some_value',
])
@pytest.mark.parametrize('body', [
    'nested = {0} + 1',
    '{0} = {0} + 2',
    'print({0})',
    '{0}.attribute',
    '{0}.method()',
    'assert {0}',
    'return {0}',
])
@pytest.mark.parametrize('code', [
    regular_function_argument,
    regular_function_default,
    regular_function_args,
    regular_function_kwargs,
    regular_function_kwonly_default,
    regular_method_argument,
    regular_method_default,
    regular_method_args,
    regular_method_kwargs,
    regular_method_kwonly,
    regular_method_kwonly_default,
])
def test_unused_arguments_used(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    argument,
    body,
    code,
    default_options,
    mode,
):
    """Testing that using unused names for used arguments is restricted."""
    function_body = body.format(argument)
    tree = parse_ast_tree(mode(code.format(argument, function_body)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedArgumentIsUsedViolation])
    assert_error_text(visitor, argument)


@pytest.mark.parametrize('argument', [
    '_arg',
    '_klass',
    '_some_value',
])
@pytest.mark.parametrize('code', [
    regular_function_argument,
    regular_function_default,
    regular_function_args,
    regular_function_kwargs,
    regular_function_kwonly_default,
    regular_method_argument,
    regular_method_default,
    regular_method_args,
    regular_method_kwargs,
    regular_method_kwonly,
    regular_method_kwonly_default,
])
def test_unused_arguments_unused(
    assert_errors,
    parse_ast_tree,
    argument,
    code,
    default_options,
    mode,
):
    """Testing that using unused names are allowed."""
    tree = parse_ast_tree(mode(code.format(argument, '...')))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

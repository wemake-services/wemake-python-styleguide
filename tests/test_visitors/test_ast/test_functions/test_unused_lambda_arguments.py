# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    UnusedArgumentIsUsedViolation,
    UnusedArgumentViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionDefinitionVisitor,
)

lambda_function_argument = 'lambda {0}: {1}'
lambda_function_default = 'lambda {0}=14: {1}'
lambda_function_args = 'lambda *{0}: {1}'
lambda_function_kwargs = 'lambda **{0}: {1}'
lambda_function_kwonly = 'lambda *, {0}: {1}'
lambda_function_kwonly_default = 'lambda *, {0}=None: {1}'


@pytest.mark.parametrize('argument', [
    'arg',
    'class_',
    'klass',
    'some_value',
])
@pytest.mark.parametrize('body', [
    '{0}',
    '{0} + 10',
    'print({0})',
    '{0}.attribute',
    '{0}.method()',
])
@pytest.mark.parametrize('code', [
    lambda_function_argument,
    lambda_function_default,
    lambda_function_args,
    lambda_function_kwargs,
    lambda_function_kwonly,
])
def test_regular_arguments_used(
    assert_errors,
    parse_ast_tree,
    argument,
    body,
    code,
    default_options,
):
    """Testing that regular arguments are fine."""
    function_body = body.format(argument)
    tree = parse_ast_tree(code.format(argument, function_body))

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
    lambda_function_argument,
    lambda_function_default,
    lambda_function_args,
    lambda_function_kwargs,
    lambda_function_kwonly,
])
def test_regular_arguments_unused(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    argument,
    code,
    default_options,
):
    """Testing that regular arguments are fine."""
    tree = parse_ast_tree(code.format(argument, '...'))

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
    '{0}',
    '{0} + 10',
    'print({0})',
    '{0}.attribute',
    '{0}.method()',
])
@pytest.mark.parametrize('code', [
    lambda_function_argument,
    lambda_function_default,
    lambda_function_args,
    lambda_function_kwargs,
    lambda_function_kwonly,
    lambda_function_kwonly_default,
])
def test_unused_arguments_used(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    argument,
    body,
    code,
    default_options,
):
    """Testing that using unused names for used arguments is restricted."""
    function_body = body.format(argument)
    tree = parse_ast_tree(code.format(argument, function_body))

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
    lambda_function_argument,
    lambda_function_default,
    lambda_function_args,
    lambda_function_kwargs,
    lambda_function_kwonly,
    lambda_function_kwonly_default,
])
def test_unused_arguments_unused(
    assert_errors,
    parse_ast_tree,
    argument,
    code,
    default_options,
):
    """Testing that underscored variables are allowed."""
    tree = parse_ast_tree(code.format(argument, '...'))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

from typing import List, NamedTuple

import pytest

from wemake_python_styleguide.violations import oop
from wemake_python_styleguide.visitors.ast.classes import WrongMethodVisitor

regular_method_detailed = """
class Useless(object):
    {decorator}
    def function(self, {args_definition}):
        {statements}
        return super({super_args}).{method_name}({args_invocation})
"""

regular_method_short = """
class Useless(object):
    def function({args}):
        {statement}
"""

TestMethodArgs = NamedTuple('TestMethodArgs', definition=str, invocation=str)


valid_method_args: List[TestMethodArgs] = [
    TestMethodArgs('', ''),
    TestMethodArgs('a', 'a'),
    TestMethodArgs('a, b', 'a, b'),
    TestMethodArgs('a, *, b', 'a, b=b'),
    TestMethodArgs('*, a, b', 'a=a, b=b'),
    TestMethodArgs('*, a, b', 'b=b, a=a'),
    TestMethodArgs('a, *args', 'a, *args'),
    TestMethodArgs('a, *args, **kwargs', 'a, *args, **kwargs'),
    TestMethodArgs('*, a, **kwargs', 'a=a, **kwargs'),
    TestMethodArgs('*, a, **kwargs', '**kwargs, a=a'),
]

valid_statements = [
    '"""Valid docstring."""',
    '',
]

valid_super_args = (
    '',
    'Useless, self',
    'Useless, obj=self',
    't=Useless, obj=self',
    'obj=self, t=Useless',
)


invalid_method_args: List[TestMethodArgs] = [
    TestMethodArgs('', 'a=1'),
    TestMethodArgs('', '1'),
    TestMethodArgs('a', ''),
    TestMethodArgs('a', 'a, 1'),
    TestMethodArgs('a, b', 'a'),
    TestMethodArgs('a, b', 'b, a=1'),
    TestMethodArgs('a, b', 'a, b, 1'),
    TestMethodArgs('a, b', 'a, b=1'),
    TestMethodArgs('a, *, b', 'a'),
    TestMethodArgs('a, *, b', '1, b'),
    TestMethodArgs('a, *, b', 'a, b=1'),
    TestMethodArgs('a, *, b', 'a=1, b=b'),
    TestMethodArgs('a, *, b', 'a, b=b, c=1'),
    TestMethodArgs('*, a, b', 'a=1, b=b'),
    TestMethodArgs('*, a, b', 'a=a, b=1'),
    TestMethodArgs('*, a, b', 'b=1, a=a'),
    TestMethodArgs('*, a, b', 'b=b, a=1'),
    TestMethodArgs('a, *args', 'a'),
    TestMethodArgs('a, *args', 'a, 1, *args'),
    TestMethodArgs('a, *args', '1, *args'),
    TestMethodArgs('a, *args', 'a=1, *args'),
    TestMethodArgs('a, *args, **kwargs', 'a'),
    TestMethodArgs('a, *args, **kwargs', 'a, *args'),
    TestMethodArgs('a, *args, **kwargs', 'a, 1, *args, **kwargs'),
    TestMethodArgs('a, *args, **kwargs', '1, *args, **kwargs'),
    TestMethodArgs('a, *args, **kwargs', 'a, *args, b=1, **kwargs'),
    TestMethodArgs('a, *args, **kwargs', 'a=1, *args, **kwargs'),
    TestMethodArgs('*, a, **kwargs', 'a=a'),
    TestMethodArgs('*, a, **kwargs', '**kwargs'),
    TestMethodArgs('*, a, **kwargs', 'a=a, b=1, **kwargs'),
]

invalid_statements = [
    'print(1)',
    'a = 1',
    'self.other()',
    '"""Docstring."""; print(1)',
]

invalid_super_args = (
    'Useless',
    'Useless, object',
    'Useless(), self',
    'Useless, obj=object',
    't=Useless, obj=object',
    't=Useless(), obj=self',
    'Useless(), obj=self',
    't=Useless, obj=self, unknown=1',
    't=Useless, incorrect=self',
)


@pytest.mark.parametrize('code', [
    regular_method_detailed,
])
@pytest.mark.parametrize('statements', valid_statements)
@pytest.mark.parametrize('method_args', valid_method_args)
@pytest.mark.parametrize('super_args', valid_super_args)
def test_useless_overwriting(
    assert_errors,
    parse_ast_tree,
    mode,
    code,
    statements,
    super_args,
    method_args,
    default_options,
):
    """Testing situations with useless overwriting."""
    formatted_code = mode(code.format(
        decorator='',
        args_definition=method_args.definition,
        statements=statements,
        super_args=super_args,
        method_name='function',
        args_invocation=method_args.invocation,
    ))
    tree = parse_ast_tree(formatted_code)

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [oop.UselessOverwrittenMethodViolation])


@pytest.mark.parametrize('code', [
    regular_method_detailed,
])
@pytest.mark.parametrize('decorator', [
    '@decorator',
])
@pytest.mark.parametrize('statements', valid_statements)
@pytest.mark.parametrize('method_args', valid_method_args)
@pytest.mark.parametrize('super_args', valid_super_args)
def test_useful_due_to_invalid_decorator(
    assert_errors,
    parse_ast_tree,
    mode,
    decorator,
    code,
    statements,
    super_args,
    method_args,
    default_options,
):
    """Testing situations with useful overwriting due to invalid decorator."""
    formatted_code = mode(code.format(
        decorator=decorator,
        args_definition=method_args.definition,
        statements=statements,
        super_args=super_args,
        method_name='function',
        args_invocation=method_args.invocation,
    ))
    tree = parse_ast_tree(formatted_code)

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    regular_method_detailed,
])
@pytest.mark.parametrize('statements', invalid_statements)
@pytest.mark.parametrize('method_args', valid_method_args)
@pytest.mark.parametrize('super_args', valid_super_args)
def test_useful_due_to_invalid_statements(
    assert_errors,
    parse_ast_tree,
    mode,
    code,
    statements,
    super_args,
    method_args,
    default_options,
):
    """Testing situations with useful overwriting due to invalid statements."""
    formatted_code = mode(code.format(
        decorator='',
        args_definition=method_args.definition,
        statements=statements,
        super_args=super_args,
        method_name='function',
        args_invocation=method_args.invocation,
    ))
    tree = parse_ast_tree(formatted_code)

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    regular_method_detailed,
])
@pytest.mark.parametrize('statements', valid_statements)
@pytest.mark.parametrize('method_args', valid_method_args)
@pytest.mark.parametrize('super_args', invalid_super_args)
def test_useful_due_to_invalid_super_args(
    assert_errors,
    parse_ast_tree,
    mode,
    code,
    statements,
    super_args,
    method_args,
    default_options,
):
    """Testing situations with useful overwriting due to invalid super args."""
    formatted_code = mode(code.format(
        decorator='',
        args_definition=method_args.definition,
        statements=statements,
        super_args=super_args,
        method_name='function',
        args_invocation=method_args.invocation,
    ))
    tree = parse_ast_tree(formatted_code)

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    regular_method_detailed,
])
@pytest.mark.parametrize('statements', valid_statements)
@pytest.mark.parametrize('method_args', valid_method_args)
@pytest.mark.parametrize('super_args', valid_super_args)
def test_useful_due_to_invalid_method(
    assert_errors,
    parse_ast_tree,
    mode,
    code,
    statements,
    super_args,
    method_args,
    default_options,
):
    """Testing situations with useful overwriting due to invalid method."""
    formatted_code = mode(code.format(
        decorator='',
        args_definition=method_args.definition,
        statements=statements,
        super_args=super_args,
        method_name='invalid_function',
        args_invocation=method_args.invocation,
    ))
    tree = parse_ast_tree(formatted_code)

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    regular_method_detailed,
])
@pytest.mark.parametrize('statements', valid_statements)
@pytest.mark.parametrize('method_args', invalid_method_args)
@pytest.mark.parametrize('super_args', valid_super_args)
def test_useful_due_to_invalid_method_args(
    assert_errors,
    parse_ast_tree,
    mode,
    code,
    statements,
    super_args,
    method_args,
    default_options,
):
    """Testing situations with useful overwriting due to invalid method args."""
    formatted_code = mode(code.format(
        decorator='',
        args_definition=method_args.definition,
        statements=statements,
        super_args=super_args,
        method_name='function',
        args_invocation=method_args.invocation,
    ))
    tree = parse_ast_tree(formatted_code)

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    regular_method_short,
])
@pytest.mark.parametrize('args,statement', (
    ('self', '""""""'),
    ('self', 'return 1'),
    ('self', 'return Useless.function()'),
    ('self', 'return Useless().function()'),
    ('self', 'return Useless()().function()'),
    ('this', 'return super().function()'),
))
def test_useful_due_to_incorrect_main_statement(
    assert_errors,
    parse_ast_tree,
    mode,
    code,
    args,
    statement,
    default_options,
):
    """Testing useful overwriting due to totally different body."""
    formatted_code = mode(code.format(args=args, statement=statement))
    tree = parse_ast_tree(formatted_code)

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

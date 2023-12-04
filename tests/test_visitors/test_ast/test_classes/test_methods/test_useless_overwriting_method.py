from typing import List, NamedTuple

import pytest

from wemake_python_styleguide.violations import oop
from wemake_python_styleguide.visitors.ast.classes import WrongMethodVisitor

regular_method_detailed = """
class Useless(object):
    {decorator}
    def function(self, {args_definition}):
        {statements}
        super({super_args}).{method_name}({args_invocation})
"""

regular_method_detailed_with_return = """
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

regular_method_short_with_extra = """
class Useless(object):
    def function({args}):
        {statement}
        return None
"""

_MethodArgs = NamedTuple('_MethodArgs', definition=str, invocation=str)

valid_method_args: List[_MethodArgs] = [
    _MethodArgs('', ''),
    _MethodArgs('a', 'a'),
    _MethodArgs('a, b', 'a, b'),
    _MethodArgs('a, *, b', 'a, b=b'),
    _MethodArgs('*, a, b', 'a=a, b=b'),
    _MethodArgs('*, a, b', 'b=b, a=a'),
    _MethodArgs('a, *args', 'a, *args'),
    _MethodArgs('a, *args, **kwargs', 'a, *args, **kwargs'),
    _MethodArgs('*, a, **kwargs', 'a=a, **kwargs'),
    _MethodArgs('*, a, **kwargs', '**kwargs, a=a'),

    _MethodArgs('/, a, b', 'a, b'),
    _MethodArgs('a, /, b', 'a, b'),
    _MethodArgs('a, b, /', 'a, b'),
    _MethodArgs('a, /, b, *, c', 'a, b, c=c'),
    _MethodArgs('a, /, b, *args, **kwargs', 'a, b, *args, **kwargs'),
    _MethodArgs('a, /, b, *arg, c, **kw', 'a, b, *arg, **kw, c=c'),
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


invalid_method_args: List[_MethodArgs] = [
    _MethodArgs('', 'a=1'),
    _MethodArgs('', '1'),
    _MethodArgs('a', ''),
    _MethodArgs('a', 'a, 1'),
    _MethodArgs('a, b', 'a'),
    _MethodArgs('a, b', 'a, b, 1'),
    _MethodArgs('a, b', 'a, b=1'),
    _MethodArgs('a, *, b', 'a'),
    _MethodArgs('a, *, b', '1, b'),
    _MethodArgs('a, *, b', 'a, b=1'),
    _MethodArgs('a, *, b', 'a=1, b=b'),
    _MethodArgs('a, *, b', 'a, b=b, c=1'),
    _MethodArgs('*, a, b', 'a=a, b=1'),
    _MethodArgs('*, a, b', 'b=b, a=1'),
    _MethodArgs('a, *args', 'a'),
    _MethodArgs('a, *args', 'a, 1, *args'),
    _MethodArgs('a, *args', 'a=1, *args'),
    _MethodArgs('a, *args, **kwargs', 'a'),
    _MethodArgs('a, *args, **kwargs', 'a, *args'),
    _MethodArgs('a, *args, **kwargs', 'a, *args, **kwargs2'),
    _MethodArgs('a, *args, **kwargs', 'a, *args2, **kwargs'),
    _MethodArgs('a, *args, **kwargs', 'a, 1, *args, **kwargs'),
    _MethodArgs('a, *args, **kwargs', '1, *args, **kwargs'),
    _MethodArgs('a, *args, **kwargs', 'a, *args, b=1, **kwargs'),
    _MethodArgs('a, *args, **kwargs', 'a=1, *args, **kwargs'),
    _MethodArgs('*, a, **kwargs', 'a=a'),
    _MethodArgs('*, a, **kwargs', '**kwargs'),
    _MethodArgs('*, a, **kwargs', 'a=a, b=1, **kwargs'),
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
    regular_method_detailed_with_return,
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
    regular_method_detailed_with_return,
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
    regular_method_detailed_with_return,
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
    regular_method_detailed_with_return,
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
    regular_method_detailed_with_return,
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
    regular_method_detailed_with_return,
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
    regular_method_short_with_extra,
])
@pytest.mark.parametrize(('args', 'statement'), [
    ('self', '""""""'),
    ('self', 'return 1'),
    ('self', 'return Useless.function()'),
    ('self', 'return Useless().function()'),
    ('self', 'return Useless()().function()'),
    ('this', 'return super().function()'),
])
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

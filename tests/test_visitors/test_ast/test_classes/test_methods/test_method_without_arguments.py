import pytest

from wemake_python_styleguide.violations.oop import (
    MethodWithoutArgumentsViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongMethodVisitor

method_inside_class = """
class Example(object):
    def some_name({0}): ...
"""

regular_function = 'def some_name({0}): ...'


def test_method_without_arguments(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    mode,
    default_options,
):
    """Testing that no arguments for method raises a violation."""
    tree = parse_ast_tree(mode(method_inside_class.format('')))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MethodWithoutArgumentsViolation])
    assert_error_text(visitor, 'some_name')


def test_function_without_arguments(
    assert_errors,
    parse_ast_tree,
    mode,
    default_options,
):
    """Testing that no arguments for method raises a violation."""
    tree = parse_ast_tree(mode(regular_function.format('')))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    method_inside_class,
    regular_function,
])
@pytest.mark.parametrize('arguments', [
    'arg1',
    'arg1=True',
    '*args',
    '**kwargs',
    '*, kwonly',
    '*, kwonly=True',
    'arg1, arg2',
])
def test_with_arguments(
    assert_errors,
    parse_ast_tree,
    code,
    arguments,
    mode,
    default_options,
):
    """Testing that other methods are working fine."""
    tree = parse_ast_tree(mode(code.format(arguments)))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

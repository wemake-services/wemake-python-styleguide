"""Test magic methods that can only be async generators or standard method."""
import pytest

from wemake_python_styleguide.violations.oop import AsyncMagicMethodViolation
from wemake_python_styleguide.violations.oop import YieldMagicMethodViolation
from wemake_python_styleguide.visitors.ast.classes import WrongMethodVisitor

sync_method = """
class Example(object):
    def {0}(self, *args, **kwargs):
        {1}
"""

async_method = """
class Example(object):
    async def {0}(self, *args, **kwargs):
        {1}
"""


@pytest.mark.parametrize('method', [
    '__aiter__',
])
@pytest.mark.parametrize('statement', [
    'yield',
    'yield 1',
    'yield from some()',
])
def test_wrong_sync_yield_magic_used(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    method,
    statement,
):
    """Testing that the method cannot be a sync generator."""
    tree = parse_ast_tree(sync_method.format(method))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [YieldMagicMethodViolation])
    assert_error_text(visitor, method)


@pytest.mark.parametrize('method', [
    '__aiter__',
])
@pytest.mark.parametrize('statement', [
    'print()',
])
def test_wrong_async_magic_used(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    method,
    statement,
):
    """Testing that the method cannot be a coroutine."""
    tree = parse_ast_tree(async_method.format(method))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [AsyncMagicMethodViolation])
    assert_error_text(visitor, method)


@pytest.mark.parametrize('method', [
    '__aiter__',
])
@pytest.mark.parametrize('statement', [
    'yield',
    'yield 1',
])
def test_correct_async_yield_magic_used(
    assert_errors,
    parse_ast_tree,
    default_options,
    method,
    statement,
):
    """Testing that the method can be an async generator."""
    tree = parse_ast_tree(async_method.format(method))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('method', [
    '__aiter__',
])
@pytest.mark.parametrize('statement', [
    'print()',
])
def test_correct_sync_magic_used(
    assert_errors,
    parse_ast_tree,
    default_options,
    method,
    statement,
):
    """Testing that the method can be a normal method."""
    tree = parse_ast_tree(sync_method.format(method))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

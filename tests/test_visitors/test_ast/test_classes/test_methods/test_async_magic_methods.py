import pytest

from wemake_python_styleguide.violations.oop import AsyncMagicMethodViolation
from wemake_python_styleguide.visitors.ast.classes import WrongMethodVisitor

sync_method = """
class Example(object):
    def {0}(self): ...
"""

async_method = """
class Example(object):
    async def {0}(self): ...
"""


@pytest.mark.parametrize('method', [
    '__init__',
    '__eq__',
    '__lt__',
    '__enter__',
    '__exit__',
])
def test_wrong_async_magic_used(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    method,
    default_options,
):
    """Testing that some async magic methods are restricted."""
    tree = parse_ast_tree(async_method.format(method))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [AsyncMagicMethodViolation])
    assert_error_text(visitor, method)


@pytest.mark.parametrize('code', [
    sync_method,
    async_method,
])
@pytest.mark.parametrize('method', [
    '__anext__',
    '__aenter__',
    '__aexit__',
    '__custom__',
])
def test_correct_async_magic_used(
    assert_errors,
    parse_ast_tree,
    method,
    code,
    default_options,
):
    """Testing that some async magic methods are working fine."""
    tree = parse_ast_tree(code.format(method))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('method', [
    '__init__',
    '__eq__',
    '__lt__',
    '__next__',
    '__enter__',
    '__exit__',
])
def test_sync_magic_used(
    assert_errors,
    parse_ast_tree,
    method,
    default_options,
):
    """Testing that any sync magic methods are working fine."""
    tree = parse_ast_tree(sync_method.format(method))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('method', [
    'next',
    'regular',
    '__custom__',
])
def test_regular_method_used(
    assert_errors,
    parse_ast_tree,
    method,
    mode,
    default_options,
):
    """Testing that other methods are working fine."""
    tree = parse_ast_tree(mode(sync_method.format(method)))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

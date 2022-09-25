import pytest

from wemake_python_styleguide.violations.oop import AsyncMagicMethodViolation
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


@pytest.mark.parametrize('template', [
    sync_method,
    async_method,
])
@pytest.mark.parametrize('method', [
    '__aiter__',
])
@pytest.mark.parametrize('statement', [
    'yield',
    'yield 1',
])
def test_yield_is_always_allowed_in_aiter(
    assert_errors,
    parse_ast_tree,
    default_options,
    template,
    method,
    statement,
):
    """Testing that the `__aiter__` can always have `yield`."""
    tree = parse_ast_tree(template.format(method, statement))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('method', [
    '__aiter__',
])
@pytest.mark.parametrize('statement', [
    'return some_async_iterator()',
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
    tree = parse_ast_tree(async_method.format(method, statement))

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
    tree = parse_ast_tree(async_method.format(method, statement))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('method', [
    '__aiter__',
])
@pytest.mark.parametrize('statement', [
    'return some_async_iterator()',
])
def test_correct_sync_magic_used(
    assert_errors,
    parse_ast_tree,
    default_options,
    method,
    statement,
):
    """Testing that the method can be a normal method."""
    tree = parse_ast_tree(sync_method.format(method, statement))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


# Examples:

correct_nested_example = """
class Some:
    {0}def __aiter__(self):
        async def inner():
            yield 1
        return inner()
"""


@pytest.mark.parametrize('example', [
    correct_nested_example,
])
@pytest.mark.parametrize('mode', [
    # We don't use `mode()` fixture here, because we have a nested func.
    '',  # sync
    'async ',
])
def test_correct_examples(
    assert_errors,
    parse_ast_tree,
    default_options,
    example,
    mode,
):
    """Testing specific real-life examples that should be working."""
    tree = parse_ast_tree(example.format(mode))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

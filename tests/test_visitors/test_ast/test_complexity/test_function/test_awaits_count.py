import pytest

from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
    TooManyAwaitsViolation,
)

function_without_awaits = 'def function(): ...'
function_async_without_awaits = 'async def function(): ...'

function_with_awaits = """
async def function():
    if 1 > 2:
        await some()
    await other()
"""

function_with_nested_function_and_awaits = """
async def function():  # has two awaits
    async def factory():  # has one await
        var_one = await one()
    await two()
"""


@pytest.mark.parametrize('code', [
    function_without_awaits,
    function_async_without_awaits,
    function_with_awaits,
    function_with_nested_function_and_awaits,
])
def test_awaits_correct_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that awaits counted correctly."""
    tree = parse_ast_tree(code)

    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_with_awaits,
    function_with_nested_function_and_awaits,
])
def test_awaits_wrong_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    options,
    code,
):
    """Testing that many awaits raises a warning."""
    tree = parse_ast_tree(code)

    option_values = options(max_awaits=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyAwaitsViolation])
    assert_error_text(visitor, '2', option_values.max_awaits)

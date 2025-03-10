import pytest

from wemake_python_styleguide.violations.best_practices import (
    AwaitInLoopViolation,
)
from wemake_python_styleguide.visitors.ast.loops import (
    WrongStatementInLoopVisitor,
)

simple_for_loop = """
async def foo():
    for _ in range(10):
        await some()
"""

list_comprehension = """
async def foo():
    result = [await some() for _ in range(10)]
"""

set_comprehension = """
async def foo():
    result = {await some() for _ in range(10)}
"""

dict_comprehension = """
async def foo():
    result = {i: await some() for i in range(10)}
"""

generator_comprehension = """
async def foo():
    result = (await some() for i in range(10))
"""

async_and_list_comprehension_in_one = """
async def foo():
    result = [
        await some_three(something_2)
        for something_1 in some_one()
        async for something_2 in some_two(something_1)
    ]
"""

# Correct:

while_loop = """
async def foo():
    while True:
        await some()
        break
"""

async_for_loop = """
async def foo():
    async for _ in some_one():
        await some_two()
"""

async_list_comprehension = """
async def foo():
    result = [await some_two() async for _ in some_one()]
"""

async_dict_comprehension = """
async def foo():
    result = {i: await some_two() async for i in some_one()}
"""

async_set_comprehension = """
async def foo():
    result = {await some_two() async for i in some_one()}
"""

async_generator_comprehension = """
async def foo():
    result = (await some_two() async for i in some_one())
"""


@pytest.mark.parametrize(
    'code',
    [
        simple_for_loop,
        list_comprehension,
        dict_comprehension,
        generator_comprehension,
        async_and_list_comprehension_in_one,
    ],
)
def test_wrong_await_in_loop(
    assert_errors,
    default_options,
    parse_ast_tree,
    code,
):
    """Tests for nested ``await`` statement in ``for`` loop."""
    tree = parse_ast_tree(code)

    visitor = WrongStatementInLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [AwaitInLoopViolation])


@pytest.mark.parametrize(
    'code',
    [
        while_loop,
        async_for_loop,
        async_list_comprehension,
        async_dict_comprehension,
        async_set_comprehension,
        async_generator_comprehension,
    ],
)
def test_good_await_in_loop(
    assert_errors,
    default_options,
    parse_ast_tree,
    code,
):
    """Tests for nested ``await`` statement in ``for`` loop."""
    tree = parse_ast_tree(code)

    visitor = WrongStatementInLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

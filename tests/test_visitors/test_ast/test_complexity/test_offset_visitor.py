# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.offset import (
    OffsetVisitor,
    TooDeepNestingViolation,
)

nested_if = """
def container():
    if True:
        x = 1
"""

nested_if2 = """
def container():
    if some_value:
        call_other()
"""

nested_for = """
def container():
    for i in '123':
        return 0
"""

nested_try = """
def container():
    try:
        some_call()
    except Exception:
        raise
"""

nested_try2 = """
def container():
    if some_call:
        try:
            some_call()
        except Exception:
            raise
"""

nested_with = """
if True:
    with open('some') as temp:
        temp.read()
"""


nested_while = """
while True:
    while True:
        continue
"""


nested_asyncfor = """
async def container():
    async for data in cursor:
        pass
"""


nested_asyncwith = """
async def container():
    async with open('some') as temp:
        pass
"""

nested_await = """
async def container1():
    async def container2():
        await cursor
"""


@pytest.mark.parametrize('code', [
    nested_if,
    nested_if2,
    nested_for,
    nested_try,
    nested_try2,
    nested_with,
    nested_while,
    nested_asyncfor,
    nested_asyncwith,
    nested_await,
])
def test_nested_offset(assert_errors, parse_ast_tree, code, default_options):
    """Testing that nested expression with default options works well."""
    tree = parse_ast_tree(code)

    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code, number_of_errors', [
    (nested_if, 1),
    (nested_if2, 1),
    (nested_for, 1),
    (nested_try, 2),
    (nested_try2, 4),
    (nested_with, 1),
    (nested_while, 1),
    (nested_asyncfor, 1),
    (nested_asyncwith, 1),
    (nested_await, 2),
])
def test_nested_offset_errors(
    assert_errors, parse_ast_tree, code, number_of_errors, options,
):
    """Testing that nested expressions are restricted."""
    tree = parse_ast_tree(code)

    option_values = options(max_offset_blocks=1)
    visitor = OffsetVisitor(option_values, tree=tree)
    visitor.run()

    errors = [TooDeepNestingViolation for _ in range(number_of_errors)]
    assert_errors(visitor, errors)


def test_regression_282(assert_errors, parse_ast_tree, options):
    """
    Testing that issue-282 will not happen again.

    See: https://github.com/wemake-services/wemake-python-styleguide/issues/282
    """
    tree = parse_ast_tree("""
    async def no_offset():
        ...
    """)

    option_values = options(max_offset_blocks=1)
    visitor = OffsetVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

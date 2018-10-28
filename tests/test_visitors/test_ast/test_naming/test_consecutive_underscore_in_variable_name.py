# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import (
    ConsecutiveUnderscoresInNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor

variable_test = """
{0} = 'test'
"""

underscore_variable_test1 = """
_{0} = 'test'
"""

underscore_variable_test2 = """
{0}_ = 'test'
"""

for_variable_test = """
for {0} in []:
    print()
"""

function_test = """
def {0}():
    ...
"""

async_function_test = """
async def {0}():
    ...
"""

argument_test = """
def some_function({0}):
    ...
"""

async_for_variable_test = """
async def container():
    async for {0} in []:
        print()
"""

with_variable_test = """
with open('test.py') as {0}:
    raise ValueError()
"""

async_with_variable_test = """
async def container():
    async with open('test.py') as {0}:
        raise ValueError()
"""

exception_test = """
try:
    1 / 0
except Exception as {0}:
    raise
"""


@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    function_test,
    async_for_variable_test,
    argument_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
])
def test_consecutive_underscores_in_variable_name(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that variable can not have private names."""
    tree = parse_ast_tree(code.format('some__value'))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConsecutiveUnderscoresInNameViolation])

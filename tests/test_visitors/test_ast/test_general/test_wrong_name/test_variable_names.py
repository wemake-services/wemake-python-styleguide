# -*- coding: utf-8 -*-

import string

import pytest

from wemake_python_styleguide.violations.naming import (
    PrivateNameViolation,
    TooShortVariableNameViolation,
    WrongVariableNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming import (
    BAD_VARIABLE_NAMES,
    WrongNameVisitor,
)

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


@pytest.mark.parametrize('bad_name', BAD_VARIABLE_NAMES)
@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
    underscore_variable_test1,
    underscore_variable_test2,
])
def test_wrong_variable_names(
    assert_errors, parse_ast_tree, bad_name, code, default_options,
):
    """Testing that variable can not have blacklisted names."""
    tree = parse_ast_tree(code.format(bad_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongVariableNameViolation])


@pytest.mark.parametrize('short_name', string.ascii_letters)
@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
])
def test_too_short_variable_names(
    assert_errors, parse_ast_tree, short_name, code, default_options,
):
    """Testing that variable can not have too short names."""
    tree = parse_ast_tree(code.format(short_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooShortVariableNameViolation])


@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
])
def test_too_short_variable_names_configured(
    assert_errors, parse_ast_tree, code, options,
):
    """Testing that variable length can be configured."""
    tree = parse_ast_tree(code.format('kira'))

    option_values = options(min_variable_length=5)
    visitor = WrongNameVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooShortVariableNameViolation])


@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
])
def test_private_variable_names(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that variable can not have private names."""
    tree = parse_ast_tree(code.format('__private_value'))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [PrivateNameViolation])


@pytest.mark.parametrize('correct_name', ['correct_name', 'xy', '_'])
@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
    underscore_variable_test1,
    underscore_variable_test2,
])
def test_correct_variable_name(
    assert_errors, parse_ast_tree, code, correct_name, default_options,
):
    """Testing that variable can have normal names."""
    tree = parse_ast_tree(code.format(correct_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import string

import pytest

from wemake_python_styleguide.violations.naming import (
    ConsecutiveUnderscoresInNameViolation,
    PrivateNameViolation,
    TooShortNameViolation,
    UnderscoredNumberNameViolation,
    WrongVariableNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming import (
    VARIABLE_NAMES_BLACKLIST,
    WrongNameVisitor,
)

variable_test = """
{0} = 'test'
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


@pytest.mark.parametrize('bad_name', VARIABLE_NAMES_BLACKLIST)
@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
])
def test_wrong_variable_names(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    bad_name,
    code,
    default_options,
):
    """Testing that variable can not have blacklisted names."""
    tree = parse_ast_tree(code.format(bad_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongVariableNameViolation])
    assert_error_text(visitor, bad_name)


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
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    short_name,
    code,
    default_options,
):
    """Testing that variable can not have too short names."""
    tree = parse_ast_tree(code.format(short_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooShortNameViolation])
    assert_error_text(visitor, short_name)


@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
])
def test_too_short_variable_names_configured(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Testing that variable length can be configured."""
    tree = parse_ast_tree(code.format('kira'))

    option_values = options(min_name_length=5)
    visitor = WrongNameVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooShortNameViolation])


@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
])
def test_private_variable_names(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that variable can not have private names."""
    private_name = '__private_value'
    tree = parse_ast_tree(code.format(private_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [PrivateNameViolation])
    assert_error_text(visitor, private_name)


@pytest.mark.parametrize('underscored_name', [
    'number_5',
    'number_4_suffix',
])
@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
])
def test_underscored_number_in_variable_names(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    underscored_name,
    code,
    default_options,
):
    """Testing that variable can not have private names."""
    tree = parse_ast_tree(code.format(underscored_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnderscoredNumberNameViolation])
    assert_error_text(visitor, underscored_name)


@pytest.mark.parametrize('underscored_name', [
    'some__name',
    'double__under__score',
    'multiple___underscores',
])
@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
])
def test_consecutive_underscores_in_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    underscored_name,
    code,
    default_options,
):
    """Testing that variable can not have private names."""
    tree = parse_ast_tree(code.format(underscored_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConsecutiveUnderscoresInNameViolation])
    assert_error_text(visitor, underscored_name)


@pytest.mark.parametrize('correct_name', [
    'correct_name',
    '_protected_name',
    'xy',
    '_',
    'test34',
    'test34_554',
])
@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    async_for_variable_test,
    with_variable_test,
    async_with_variable_test,
    exception_test,
])
def test_correct_variable_name(
    assert_errors,
    parse_ast_tree,
    code,
    correct_name,
    default_options,
):
    """Testing that variable can have normal names."""
    tree = parse_ast_tree(code.format(correct_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import string

import pytest

from wemake_python_styleguide.visitors.wrong_name import (
    BAD_VARIABLE_NAMES,
    PrivateNameViolation,
    TooShortVariableNameViolation,
    WrongNameVisitor,
    WrongVariableNameViolation,
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

with_variable_test = """
with open('test.py') as {0}:
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
    with_variable_test,
    exception_test,
    underscore_variable_test1,
    underscore_variable_test2,
])
def test_wrong_variable_names(
    assert_errors, parse_ast_tree, bad_name, code, default_options,
):
    """Testing that variable can not have blacklisted names."""
    tree = parse_ast_tree(code.format(bad_name))

    visiter = WrongNameVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [WrongVariableNameViolation])


@pytest.mark.parametrize('short_name', string.ascii_letters)
@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    with_variable_test,
    exception_test,
])
def test_too_short_variable_names(
    assert_errors, parse_ast_tree, short_name, code, default_options,
):
    """Testing that variable can not have too short names."""
    tree = parse_ast_tree(code.format(short_name))

    visiter = WrongNameVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [TooShortVariableNameViolation])


@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    with_variable_test,
    exception_test,
])
def test_too_short_variable_names_configured(
    assert_errors, parse_ast_tree, code, options,
):
    """Testing that variable length can be configured."""
    tree = parse_ast_tree(code.format('some'))

    option_values = options(min_variable_length=5)
    visiter = WrongNameVisitor(option_values)
    visiter.visit(tree)

    assert_errors(visiter, [TooShortVariableNameViolation])


@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    with_variable_test,
    exception_test,
])
def test_private_variable_names(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that variable can not have private names."""
    tree = parse_ast_tree(code.format('__private_value'))

    visiter = WrongNameVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [PrivateNameViolation])


@pytest.mark.parametrize('correct_name', ['correct_name', 'xy', '_'])
@pytest.mark.parametrize('code', [
    variable_test,
    for_variable_test,
    with_variable_test,
    exception_test,
    underscore_variable_test1,
    underscore_variable_test2,
])
def test_correct_variable_name(
    assert_errors, parse_ast_tree, code, correct_name, default_options,
):
    """Testing that variable can have normal names."""
    tree = parse_ast_tree(code.format(correct_name))

    visiter = WrongNameVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])

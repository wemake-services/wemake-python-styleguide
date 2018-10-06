# -*- coding: utf-8 -*-

import string

import pytest

from wemake_python_styleguide.violations.naming import (
    PrivateNameViolation,
    TooShortVariableNameViolation,
    WrongVariableNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming import (
    VARIABLE_NAMES_BLACKLIST,
    WrongNameVisitor,
)

function_name = """
def {0}(): ...
"""

async_function_name = """
async def {0}(): ...
"""

method_name = """
class Input:
    def {0}(self): ...
"""


@pytest.mark.parametrize('bad_name', VARIABLE_NAMES_BLACKLIST)
@pytest.mark.parametrize('code', [
    function_name,
    async_function_name,
    method_name,
])
def test_wrong_function_names(
    assert_errors, parse_ast_tree, bad_name, code, default_options,
):
    """Testing that function can not have blacklisted names."""
    tree = parse_ast_tree(code.format(bad_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongVariableNameViolation])


@pytest.mark.parametrize('short_name', string.ascii_letters)
@pytest.mark.parametrize('code', [
    function_name,
    async_function_name,
    method_name,
])
def test_too_short_function_names(
    assert_errors, parse_ast_tree, short_name, code, default_options,
):
    """Testing that function can not have too short names."""
    tree = parse_ast_tree(code.format(short_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooShortVariableNameViolation])


@pytest.mark.parametrize('code', [
    function_name,
    async_function_name,
    method_name,
])
def test_private_function_names(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that function can not have private names."""
    tree = parse_ast_tree(code.format('__hidden'))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [PrivateNameViolation])


@pytest.mark.parametrize('correct_name', [
    'my_function',
    'xy',
    'test',
    '_protected',
    '__magic__',
])
@pytest.mark.parametrize('code', [
    function_name,
    async_function_name,
    method_name,
])
def test_correct_function_names(
    assert_errors, parse_ast_tree, correct_name, code, default_options,
):
    """Testing that function can have normal names."""
    tree = parse_ast_tree(code.format(correct_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

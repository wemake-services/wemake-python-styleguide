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

function_test = """
def test({0}, {1}): ...
"""

method_test = """
class Input:
    def validate(self, {0}, {1}): ...
"""

function_kwargs_test = """
def test({0}=None, {1}=None): ...
"""

method_kwargs_test = """
class Input:
    def validate(self, {0}=None, {1}=0): ...
"""

function_args_kwargs_test = """
def test(*{0}, **{1}): ...
"""

method_args_kwargs_test = """
class Input:
    def validate(self, *{0}, **{1}): ...
"""


@pytest.mark.parametrize('bad_name', BAD_VARIABLE_NAMES)
@pytest.mark.parametrize('code', [
    function_test,
    method_test,
    function_kwargs_test,
    method_kwargs_test,
    function_args_kwargs_test,
    method_args_kwargs_test,
])
def test_wrong_function_arguments(
    assert_errors, parse_ast_tree, bad_name, code, default_options,
):
    """Testing that function can not have blacklisted arguments."""
    tree = parse_ast_tree(code.format('x', bad_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        TooShortVariableNameViolation,
        WrongVariableNameViolation,
    ])


@pytest.mark.parametrize('short_name', string.ascii_letters)
@pytest.mark.parametrize('code', [
    function_test,
    method_test,
    function_kwargs_test,
    method_kwargs_test,
    function_args_kwargs_test,
    method_args_kwargs_test,
])
def test_too_short_function_arguments(
    assert_errors, parse_ast_tree, short_name, code, default_options,
):
    """Testing that function can not have too short arguments."""
    tree = parse_ast_tree(code.format(short_name, 'data'))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        TooShortVariableNameViolation,
        WrongVariableNameViolation,
    ])


@pytest.mark.parametrize('code', [
    function_test,
    method_test,
    function_kwargs_test,
    method_kwargs_test,
    function_args_kwargs_test,
    method_args_kwargs_test,
])
def test_private_function_arguments(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that function can not have private arguments."""
    tree = parse_ast_tree(code.format('__private', '__name'))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        PrivateNameViolation,
        PrivateNameViolation,
    ])


@pytest.mark.parametrize('code', [
    function_test,
    method_test,
    function_kwargs_test,
    method_kwargs_test,
    function_args_kwargs_test,
    method_args_kwargs_test,
])
def test_correct_function_arguments(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that function can have normal arguments."""
    tree = parse_ast_tree(code.format('xy', 'normal_name'))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

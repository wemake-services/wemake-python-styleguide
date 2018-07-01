# -*- coding: utf-8 -*-

import string

import pytest

from wemake_python_styleguide.visitors.wrong_name import (
    BAD_VARIABLE_NAMES,
    TooShortFunctionNameViolation,
    WrongFunctionNameViolation,
    WrongNameVisitor,
)

function_bad_name = """
def {0}(): ...
"""

method_bad_name = """
class Input:
    def {0}(self): ...
"""


@pytest.mark.parametrize('bad_name', BAD_VARIABLE_NAMES)
@pytest.mark.parametrize('code', [
    function_bad_name,
    method_bad_name,
])
def test_wrong_function_names(
    assert_errors, parse_ast_tree, bad_name, code,
):
    """Testing that function can not have blacklisted names."""
    tree = parse_ast_tree(code.format(bad_name))

    visiter = WrongNameVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [WrongFunctionNameViolation])


@pytest.mark.parametrize('short_name', string.ascii_letters)
@pytest.mark.parametrize('code', [
    function_bad_name,
    method_bad_name,
])
def test_too_short_function_names(
    assert_errors, parse_ast_tree, short_name, code,
):
    """Testing that function can not have too short names."""
    tree = parse_ast_tree(code.format(short_name))

    visiter = WrongNameVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [TooShortFunctionNameViolation])


@pytest.mark.parametrize('correct_name', ['my_function', 'xy', 'test'])
@pytest.mark.parametrize('code', [
    function_bad_name,
    method_bad_name,
])
def test_correct_function_name(
    assert_errors, parse_ast_tree, correct_name, code,
):
    """Testing that function can have normal names."""
    tree = parse_ast_tree(code.format(correct_name))

    visiter = WrongNameVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])

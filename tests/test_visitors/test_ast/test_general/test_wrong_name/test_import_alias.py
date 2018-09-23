# -*- coding: utf-8 -*-

import string

import pytest

from wemake_python_styleguide.visitors.ast.general.wrong_name import (
    BAD_VARIABLE_NAMES,
    PrivateNameViolation,
    TooShortVariableNameViolation,
    WrongNameVisitor,
    WrongVariableNameViolation,
)

import_alias = """
import os as {0}
"""

from_import_alias = """
from os import path as {0}
"""


@pytest.mark.parametrize('bad_name', BAD_VARIABLE_NAMES)
@pytest.mark.parametrize('code', [
    import_alias,
    from_import_alias,
])
def test_wrong_import_alias_names(
    assert_errors, parse_ast_tree, bad_name, code, default_options,
):
    """Testing that import aliases can not have blacklisted names."""
    tree = parse_ast_tree(code.format(bad_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongVariableNameViolation])


@pytest.mark.parametrize('short_name', string.ascii_letters)
@pytest.mark.parametrize('code', [
    import_alias,
    from_import_alias,
])
def test_too_short_import_alias_names(
    assert_errors, parse_ast_tree, short_name, code, default_options,
):
    """Testing that import aliases can not have too short names."""
    tree = parse_ast_tree(code.format(short_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooShortVariableNameViolation])


@pytest.mark.parametrize('code', [
    import_alias,
    from_import_alias,
])
def test_private_import_alias_names(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that import aliases can not have too private names."""
    tree = parse_ast_tree(code.format('__hidden'))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [PrivateNameViolation])


@pytest.mark.parametrize('correct_name', [
    'my_alias',
    'xy',
    'test',
    '_protected',
])
@pytest.mark.parametrize('code', [
    import_alias,
    from_import_alias,
])
def test_correct_import_alias_names(
    assert_errors, parse_ast_tree, correct_name, code, default_options,
):
    """Testing that import aliases can have normal names."""
    tree = parse_ast_tree(code.format(correct_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    AlphabetAsStringViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import WrongStringVisitor

GOOD_STRING1 = 'aBcDeFGHiJKLMNOPQRSTUVWXYZ'
GOOD_STRING2 = 'aBNOhQtYZ'


@pytest.mark.parametrize('code', [
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'abcdefghijklmnopqrstuvwxyz',
])  # noqa: WPS449
def test_alphabet_as_string_violation(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that the strings violate the rules."""
    tree = parse_ast_tree(code)
    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [AlphabetAsStringViolation])


@pytest.mark.parametrize('code', [GOOD_STRING1, GOOD_STRING2])
def test_alphabet_as_string_no_violation(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that regular strings work well."""
    tree = parse_ast_tree(code)
    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

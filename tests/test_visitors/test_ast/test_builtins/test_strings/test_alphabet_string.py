# -*- coding: utf-8 -*-

import pytest
import string

from wemake_python_styleguide.violations.best_practices import (
    AlphabetAsStringViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import WrongStringVisitor

BOTHCASES_ALPH = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
UPPERCASE_ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWERCASE_ALPH = "abcdefghijklmnopqrstuvwxyz"
GOOD_STRING1 = "aBcDeFGHiJKLMNOPQRSTUVWXYZ"
GOOD_STRING2 = "aBNOhQtYZ"


@pytest.mark.parametrize('code', [
    BOTHCASES_ALPH, UPPERCASE_ALPH, LOWERCASE_ALPH
])
def test_alphabet_as_string_violation(assert_errors, parse_ast_tree, code, default_options):

    tree = parse_ast_tree(code)
    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [AlphabetAsStringViolation])


@pytest.mark.parametrize('code', [GOOD_STRING1, GOOD_STRING2])
def test_alphabet_as_string_no_violation(assert_errors, parse_ast_tree, code, default_options):

    tree = parse_ast_tree(code)
    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

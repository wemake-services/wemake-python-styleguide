# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.general.wrong_keyword import (
    WrongKeywordViolation,
    WrongKeywordVisitor,
)

global_in_function = """
x = 0

def check_global():
    global x
"""

nonlocal_in_function = """
def check_nonlocal():
    j = 10

    def nested():
        nonlocal j
"""


@pytest.mark.parametrize('code', [
    global_in_function,
    nonlocal_in_function,
])
def test_global_keywords(assert_errors, parse_ast_tree, code, default_options):
    """Testing that `global` and `nonlocal` keywords are restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongKeywordViolation])

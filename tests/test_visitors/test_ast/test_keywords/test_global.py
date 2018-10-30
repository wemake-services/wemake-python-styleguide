# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongKeywordViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import WrongKeywordVisitor

global_in_module = """
some = 0
global some
"""

global_in_function = """
some = 0

def check_global():
    global some
"""

global_in_method = """
some = 0

class Test(object):
    def run(self):
        global some
"""

nonlocal_in_function = """
def check_nonlocal():
    some = 10

    def nested():
        nonlocal some
"""

nonlocal_in_method = """
class Test(object):
    def check_nonlocal(self):
        some = 10

        def nested():
            nonlocal some
"""


@pytest.mark.parametrize('code', [
    global_in_module,
    global_in_function,
    global_in_method,
])
def test_global_keywords(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that `global` keyword is restricted."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongKeywordViolation])
    assert_error_text(visitor, 'global')


@pytest.mark.parametrize('code', [
    nonlocal_in_function,
    nonlocal_in_method,
])
def test_nonlocal_keywords(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that `nonlocal` keyword is restricted."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongKeywordViolation])
    assert_error_text(visitor, 'nonlocal')

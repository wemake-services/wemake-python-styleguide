# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_keyword import (
    WrongKeywordViolation,
    WrongKeywordVisitor,
)

pass_function = """
def function():
    pass
"""

pass_class = """
class Test:
    pass
"""

pass_method = """
class Test:
    def method(self):
        pass
"""


@pytest.mark.parametrize('code', [
    pass_function,
    pass_class,
    pass_method,
])
def test_pass_keyword(assert_errors, parse_ast_tree, code):
    """Testing that pass keyword is restricted inside different definitions."""
    tree = parse_ast_tree(code)

    visiter = WrongKeywordVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [WrongKeywordViolation])

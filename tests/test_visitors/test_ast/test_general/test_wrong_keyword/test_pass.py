# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.general.wrong_keyword import (
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

pass_condition = """
for i in 'abc':
    if i == 'a':
        pass
    else:
        print(i)
"""


@pytest.mark.parametrize('code', [
    pass_function,
    pass_class,
    pass_method,
    pass_condition,
])
def test_pass_keyword(assert_errors, parse_ast_tree, code, default_options):
    """Testing that pass keyword is restricted inside different definitions."""
    tree = parse_ast_tree(code)

    visitor = WrongKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongKeywordViolation])

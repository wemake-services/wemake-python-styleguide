# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongKeywordViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import WrongKeywordVisitor

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

pass_exception = """
try:
    1 / 0
except Exception:
    pass
"""


@pytest.mark.parametrize('code', [
    pass_function,
    pass_class,
    pass_method,
    pass_condition,
    pass_exception,
])
def test_pass_keyword(assert_errors, parse_ast_tree, code, default_options):
    """Testing that pass keyword is restricted inside different definitions."""
    tree = parse_ast_tree(code)

    visitor = WrongKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongKeywordViolation])

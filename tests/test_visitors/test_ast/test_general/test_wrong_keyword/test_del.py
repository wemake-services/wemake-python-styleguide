# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.general.wrong_keyword import (
    WrongKeywordViolation,
    WrongKeywordVisitor,
)

del_variable = """
x = 5
del x
"""

del_key = """
temp_dict = {'a': 1}
del a['a']
"""


@pytest.mark.parametrize('code', [
    del_variable,
    del_key,
])
def test_del_keyword(assert_errors, parse_ast_tree, code, default_options):
    """Testing that `del` keyword is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongKeywordViolation])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongKeywordViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import WrongKeywordVisitor

del_variable = """
x = 5
del x
"""

del_key = """
temp_dict = {'a': 1}
del temp_dict['a']
"""

del_index = """
temp_list = [1, 2, 3]
del temp_list[0]
"""


@pytest.mark.parametrize('code', [
    del_variable,
    del_key,
    del_index,
])
def test_del_keyword(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """
    Testing that `del` keyword is restricted.

    Regression:
    https://github.com/wemake-services/wemake-python-styleguide/issues/493
    """
    tree = parse_ast_tree(code)

    visitor = WrongKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongKeywordViolation])
    assert_error_text(visitor, 'del')

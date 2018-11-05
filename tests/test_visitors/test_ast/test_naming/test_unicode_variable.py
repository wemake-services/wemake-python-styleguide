# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import UnicodeNameViolation
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor

wrong_fragment_all = """
переменная = 'variable'
"""

wrong_fragment_middle = """
test_unicode_переменная_variable = 42
"""

wrong_fragment_start = """
переменная_initialize = 42
"""

wrong_fragment_ended = """
init_переменная = 42
"""

wrong_fragment_multiple = """
test_variable = переменная = 'variable'
"""


@pytest.mark.parametrize('code', [
    wrong_fragment_all,
    wrong_fragment_ended,
    wrong_fragment_middle,
    wrong_fragment_start,
    wrong_fragment_multiple,
])
def test_variable_unicode(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Test variable name with unicode."""
    tree = parse_ast_tree(code)
    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UnicodeNameViolation])


corrrect_fragmet_all = """
some_variable = 42
test_variable = some_variable
"""


@pytest.mark.parametrize('code', [
    corrrect_fragmet_all,
])
def test_variable_correct(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Test variable name without unicode."""
    tree = parse_ast_tree(code)
    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

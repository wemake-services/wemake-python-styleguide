# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import UnicodeNameViolation
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor

wrong_fragment_all = """
def функиця():
   pass
"""

wrong_fragment_middle = """
def test_функция_test():
    pass
"""

wrong_fragment_start = """
def фукнция_test():
    pass
"""

wrong_fragment_ended = """
def test_функция():
    pass
"""


@pytest.mark.parametrize('code', [
    wrong_fragment_all,
    wrong_fragment_ended,
    wrong_fragment_middle,
    wrong_fragment_start,
])
def test_function_unicode(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Test function name with unicode."""
    tree = parse_ast_tree(code)
    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UnicodeNameViolation])


corrrect_fragmet_all = """
def correct():
    pass
"""


@pytest.mark.parametrize('code', [
    corrrect_fragmet_all,
])
def test_function_correct(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Test function name without unicode."""
    tree = parse_ast_tree(code)
    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

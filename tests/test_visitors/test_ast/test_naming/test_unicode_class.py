# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import UnicodeNameViolation
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor

wrong_fragment_all = """
class ИмяКласса():
   pass
"""

wrong_fragment_middle = """
class TestИмяКлассаTest():
    pass
"""

wrong_fragment_start = """
def ИмяКлассаTest():
    pass
"""

wrong_fragment_ended = """
def TestИмяКласса():
    pass
"""


@pytest.mark.parametrize('code', [
    wrong_fragment_all,
    wrong_fragment_ended,
    wrong_fragment_middle,
    wrong_fragment_start,
])
def test_class_unicode(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Test class name with unicode."""
    tree = parse_ast_tree(code)
    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UnicodeNameViolation])


corrrect_fragmet_all = """
def Correct():
    pass
"""


@pytest.mark.parametrize('code', [
    corrrect_fragmet_all,
])
def test_class_correct(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Test class name without unicode."""
    tree = parse_ast_tree(code)
    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

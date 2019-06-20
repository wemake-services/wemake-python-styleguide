# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    YieldInComprehensionViolation,
)
from wemake_python_styleguide.visitors.ast.loops import (
    WrongComprehensionVisitor,
)

list_comprehension = """
def container():
    nodes = [{0} for xy in "abc"]
"""

generator_expression = """
def container():
    nodes = ({0} for xy in "abc")
"""

set_comprehension = """
def container():
    nodes = {{{0} for xy in "abc"}}
"""


# We ignore `DeprecationWarning: 'yield' inside generator expression` here
@pytest.mark.filterwarnings('ignore:DeprecationWarning')
@pytest.mark.parametrize('code', [
    list_comprehension,
    generator_expression,
    set_comprehension,
])
def test_yield_keyword_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that using `yield` keyword is not allowed."""
    tree = parse_ast_tree(mode(code.format('(yield xy)')))

    visitor = WrongComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [YieldInComprehensionViolation])


@pytest.mark.parametrize('code', [
    list_comprehension,
    generator_expression,
    set_comprehension,
])
def test_comprehension_without_yield(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that regular comprehensions are allowed."""
    tree = parse_ast_tree(mode(code.format('xy')))
    visitor = WrongComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.compat.constants import PY38
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


# We ignore `DeprecationWarning: 'yield' inside generator expression` here,
# which is thrown on python3.7
# We also skip this test on python3.8, because it does not make any sence.
@pytest.mark.skipif(
    PY38,
    reason='yield inside a generator is a syntax error in python3.8',
)
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


@pytest.mark.skipif(
    not PY38,
    reason='We check for syntax error here, which is true for python3.8+',
)
@pytest.mark.parametrize('code', [
    list_comprehension,
    generator_expression,
    set_comprehension,
])
def test_yield_keyword_syntax_error(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that using `yield` keyword is not allowed."""
    with pytest.raises(SyntaxError):
        parse_ast_tree(mode(code.format('(yield xy)')))


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

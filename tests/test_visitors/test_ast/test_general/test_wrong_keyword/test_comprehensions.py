# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.general.wrong_keyword import (
    MultipleIfsInComprehensionViolation,
    WrongListComprehensionVisitor,
)

ifs_multiple = """
nodes = [node for node in 'abc' if node != 'a' if node != 'b' if node != 'c']
"""

ifs_twice = """
nodes = [node for node in 'abc' if node != 'a' if node != 'b']
"""

ifs_single = """
nodes = [node for node in 'abc' if node != 'a']
"""

without_ifs = """
nodes = [node for node in 'abc']
"""


@pytest.mark.parametrize('code', [
    ifs_single,
    without_ifs,
])
def test_if_keyword_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that using `if` keyword is allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongListComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    ifs_multiple,
    ifs_twice,
])
def test_multiple_if_keywords_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that using multiple `if` keywords is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongListComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MultipleIfsInComprehensionViolation])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    MultilineLoopViolation,
)
from wemake_python_styleguide.visitors.ast.loops import WrongLoopVisitor

incorrect_loop1 = """
def wrapper():
    for x in some_func(1,
    3):
        ...
"""

incorrect_loop2 = """
def wrapper():
    for x in [1,
    2,3,4]:
        ...
"""

incorrect_loop3 = """
while some_func(1,
3):
    ...
"""

correct_loop1 = """
def wrapper():
    for x in [1,2,3,4]:
        ...
"""

correct_loop2 = """
def wrapper():
    for x in [1,2,3,4]:
        ...
        ...
    return
"""

correct_loop3 = """
while some_func(1,3):
    ...
"""


@pytest.mark.parametrize('code', [
    incorrect_loop1,
    incorrect_loop2,
    incorrect_loop3,
])
def test_incorrect_multiline_loops(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing multiline loops."""
    tree = parse_ast_tree(mode(code))
    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [MultilineLoopViolation])


@pytest.mark.parametrize('code', [
    correct_loop1,
    correct_loop2,
    correct_loop3,
])
def test_correct_multiline_loops(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing multiline loops."""
    tree = parse_ast_tree(mode(code))
    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

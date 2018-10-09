# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.complexity import UnusedElseViolation
from wemake_python_styleguide.visitors.ast.loops import WrongForElseVisitor

wrong_else_in_for_loop = """
for x in '123':
    ...
else:
    ...
"""

right_else_in_for_loop = """
for x in '123':
    break
else:
   ...
"""

check_nested_if_else = """
for x in '123':
    if x:
        ...
    else:
        ...
"""


@pytest.mark.parametrize('code', [
    wrong_else_in_for_loop,
])
def test_wrong_else_in_for_loop(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Violations are raised when else without break statement in for loops."""
    tree = parse_ast_tree(code)

    visitor = WrongForElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedElseViolation])


@pytest.mark.parametrize('code', [
    right_else_in_for_loop,
    check_nested_if_else,
])
def test_correct_else_in_for_loop(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Violations are not raised when else with break statement in for loop."""
    tree = parse_ast_tree(code)

    visitor = WrongForElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

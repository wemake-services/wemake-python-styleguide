# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    InconsistentReturnVariablesViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    ConsistentReturningVisitor,
)

# Correct:

correct_example1 = """
def some_function():
    return 1
"""

correct_example2 = """
def some_function():
     some_value = 1
     name = last_name + first_name
     return some_value
"""

correct_example3 = """
def some_function():
     some_value = 1
     other_value = 2
     return some_value + other_value
     """

correct_example4 = """
def some_function():
     some_value = 1
     name = last_name + some_value
     return name, some_value
"""

wrong_example1 = """
def function():
     some_value = 1
     return some_value
"""


@pytest.mark.parametrize('code', [
    wrong_example1,
])
def test_wrong_return_variable(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing incorrect `return` statements."""
    tree = parse_ast_tree(mode(code))
    visitor = ConsistentReturningVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [InconsistentReturnVariablesViolation])


@pytest.mark.parametrize('code', [
    correct_example1,
    correct_example2,
    correct_example3,
    correct_example4,
])
def test_correct_return_statements(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing correct `return` statements."""
    tree = parse_ast_tree(mode(code))
    visitor = ConsistentReturningVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

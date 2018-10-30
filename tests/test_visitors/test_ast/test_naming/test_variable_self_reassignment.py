# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    ReassigningVariableToItselfViolation,
)
from wemake_python_styleguide.visitors.ast.naming import (
    WrongVariableAssignmentVisitor,
)

wrong_fragment = """
test_variable = 5
test_variable = test_variable
"""

right_fragment = """
test_variable = 5
test_variable = 10
"""

right_fragment_tuple_assignment = """
x = 1
y = 2
x, y = y, x
"""

wrong_fragment_double_assignment = """
test_variable = 5
test_variable = test_variable = 10
"""

wrong_fragment_other_assignment = """
test_variable = 5
test_variable = other = test_variable = 5
"""

wrong_fragment_tuple_assignment = """
x = 1
y = 2
x, y = x, y
"""

wrong_fragment_multiple_tuple_assignment = """
x = 1
y = 2
z = 3
x, y, z = x, y, z
"""


@pytest.mark.parametrize('code', [
    wrong_fragment,
    wrong_fragment_double_assignment,
    wrong_fragment_other_assignment,
    wrong_fragment_tuple_assignment,
    wrong_fragment_multiple_tuple_assignment,
])
def test_self_variable_reassignment(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that self variable reassignment is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongVariableAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ReassigningVariableToItselfViolation])


@pytest.mark.parametrize('code', [
    right_fragment,
    right_fragment_tuple_assignment,
])
def test_correct_variable_reassignment(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that we can do normal variable."""
    tree = parse_ast_tree(code)

    visitor = WrongVariableAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

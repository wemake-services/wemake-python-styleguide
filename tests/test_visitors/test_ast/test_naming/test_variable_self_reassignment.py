# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    ReassigningVariableToItselfViolation,
)
from wemake_python_styleguide.visitors.ast.naming import (
    WrongVariableAssignmentVisitor,
)

# Correct:

right_fragment = """
test_variable = 5
test_variable = 10
"""

right_typed_fragment = """
test_variable: int = 5
test_variable: int = 10
"""

right_fragment_tuple_assignment = """
x = 1
y = 2
x, y = y, x
"""

right_fragment_triple_tuple_assignment = """
x = 1
y = 2
z = 3
x, y, z = z, x, y
"""

right_star_assignment1 = """
x = 1
y = 2
y, *x = x, y
"""

right_star_assignment2 = """
x = 1
y = 2
x, *y = y, x
"""

right_star_assignment3 = """
x = 1
y = 2
z = 3
x, *y = z, x, y
"""

# Wrong:

wrong_fragment = """
test_variable = 5
test_variable = test_variable
"""

wrong_typed_fragment = """
test_variable: int = 5
test_variable: int = test_variable
"""

wrong_partial_typed_fragment1 = """
test_variable: int = 5
test_variable = test_variable
"""

wrong_partial_typed_fragment2 = """
test_variable = 5
test_variable: int = test_variable
"""

wrong_fragment_double_assignment = """
test_variable = 5
test_variable = test_variable = 10
"""

wrong_fragment_double_typed_assignment = """
test_variable: int = 5
test_variable = test_variable = 10
"""

wrong_fragment_other_assignment = """
test_variable = 5
test_variable = other = test_variable = 5
"""

wrong_fragment_typed_other_assignment = """
test_variable: int = 5
test_variable = other = test_variable = 5
"""

wrong_fragment_mixed_tuple_assignment = """
x = 1
y = 2
z = 3
x, y, z = x, z, y
"""

# Double wrong:

wrong_fragment_tuple_assignment = """
x = 1
y = 2
x, y = x, y
"""

wrong_fragment_typed_tuple_assignment = """
x: int = 1
y: int = 2
x, y = x, y
"""

# Triple wrong

wrong_fragment_multiple_tuple_assignment = """
x = 1
y = 2
z = 3
x, y, z = x, y, z
"""

wrong_fragment_typed_multiple_assignment = """
x: int = 1
y: int = 2
z = 3
x, y, z = x, y, z
"""


@pytest.mark.parametrize('code', [
    wrong_fragment,
    wrong_typed_fragment,
    wrong_partial_typed_fragment1,
    wrong_partial_typed_fragment2,
    wrong_fragment_double_assignment,
    wrong_fragment_double_typed_assignment,
    wrong_fragment_other_assignment,
    wrong_fragment_typed_other_assignment,
    wrong_fragment_mixed_tuple_assignment,
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
    wrong_fragment_tuple_assignment,
    wrong_fragment_typed_tuple_assignment,
])
def test_self_variable_reassignment_double(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that self variable reassignment is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongVariableAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        ReassigningVariableToItselfViolation,
        ReassigningVariableToItselfViolation,
    ])


@pytest.mark.parametrize('code', [
    wrong_fragment_multiple_tuple_assignment,
    wrong_fragment_typed_multiple_assignment,
])
def test_self_variable_reassignment_triple(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that self variable reassignment is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongVariableAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        ReassigningVariableToItselfViolation,
        ReassigningVariableToItselfViolation,
        ReassigningVariableToItselfViolation,
    ])


@pytest.mark.parametrize('code', [
    right_fragment,
    right_typed_fragment,
    right_fragment_tuple_assignment,
    right_fragment_triple_tuple_assignment,
    right_star_assignment1,
    right_star_assignment2,
    right_star_assignment3,
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

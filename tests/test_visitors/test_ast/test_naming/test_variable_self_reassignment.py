# -*- coding: utf-8 -*-

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


def test_self_variable_reassignment(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that self variable reassignment is restricted."""
    tree = parse_ast_tree(wrong_fragment)
    visitor = WrongVariableAssignmentVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [ReassigningVariableToItselfViolation])


def test_correct_variable_reassignment(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that we can do normal variable."""
    tree = parse_ast_tree(right_fragment)
    visitor = WrongVariableAssignmentVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

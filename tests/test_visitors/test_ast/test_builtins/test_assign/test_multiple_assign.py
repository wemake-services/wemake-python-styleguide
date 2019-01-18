# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    MultipleAssignmentsViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import (
    WrongAssignmentVisitor,
)

# Correct usages:

single_assignment = 'constant = 1'
tuple_assignment = 'first, second = (1, 2)'
spread_assignment = 'first, *_, second = [1, 2, 4, 3]'

# Incorrect usages:

two_assignment = 'first = second = 1'
three_assignment = 'first = second = third'


@pytest.mark.parametrize('code', [
    single_assignment,
    tuple_assignment,
    spread_assignment,
])
def test_correct_assignments(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correct assignments work."""
    tree = parse_ast_tree(code)

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    two_assignment,
    three_assignment,
])
def test_multiple_assignments(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that multiple assignments are restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MultipleAssignmentsViolation])

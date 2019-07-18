# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongUnpackingViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import (
    WrongAssignmentVisitor,
)

single_assignment = '{0} = 1'

tuple_assignment1 = 'first, {0} = (1, 2)'
tuple_assignment1 = '{0}, second = (1, 2)'

spread_assignment1 = '{0}, *second = [1, 2, 3]'
spread_assignment2 = 'first, *{0} = [1, 2, 3]'

for_assignment = """
for {0} in []:
    ...
"""

for_unpacking1 = """
for {0}, second in enumerate([]):
    ...
"""

for_unpacking2 = """
for first, {0} in enumerate([]):
    ...
"""

with_assignment = """
with some() as {0}:
    ...
"""

with_unpacking1 = """
with some() as ({0}, second):
    ...
"""

with_unpacking2 = """
with some() as (first, {0}):
    ...
"""


@pytest.mark.parametrize('code', [
    single_assignment,
    tuple_assignment1,
    tuple_assignment1,
    spread_assignment1,
    spread_assignment2,
    for_assignment,
    for_unpacking1,
    for_unpacking2,
    with_assignment,
    with_unpacking1,
    with_unpacking2,
])
def test_correct_unpacking(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correct assignments work."""
    tree = parse_ast_tree(code.format('some_name'))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('assignment', [
    'some[0]',
    'some["key"]',
    'some.attr',
])
def test_correct_assignment(
    assert_errors,
    parse_ast_tree,
    assignment,
    default_options,
):
    """Testing that correct assignments work."""
    tree = parse_ast_tree(single_assignment.format(assignment))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    tuple_assignment1,
    tuple_assignment1,
    spread_assignment1,
    spread_assignment2,
    for_unpacking1,
    for_unpacking2,
    with_unpacking1,
    with_unpacking2,
])
@pytest.mark.parametrize('assignment', [
    'some[0]',
    'some["key"]',
    'some.attr',
])
def test_multiple_assignments(
    assert_errors,
    parse_ast_tree,
    code,
    assignment,
    default_options,
):
    """Testing that multiple assignments are restricted."""
    tree = parse_ast_tree(code.format(assignment))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongUnpackingViolation])

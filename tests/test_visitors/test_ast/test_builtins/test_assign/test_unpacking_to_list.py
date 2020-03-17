import pytest

from wemake_python_styleguide.violations.best_practices import (
    MultipleAssignmentsViolation,
    WrongUnpackingViolation,
)
from wemake_python_styleguide.violations.consistency import (
    UnpackingIterableToListViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import (
    WrongAssignmentVisitor,
)

list_target = '[first, second]'
nested_list_target0 = '([first, second], third)'
nested_list_tatget1 = '(first, [second, third])'
nested_list_target2 = '(first, (second, [third, fourth]))'
multiple_level_nested_list_target = '(first, (second, [third, fourth]))'

spread_assignment_in_list_target = '[first, *rest]'
nested_spread_assignment_in_list = '(first, [second, *rest])'
multiple_level_nested_spread_assign_in_list = (
    '(first, (second, [*rest, last]))'
)

regular_assignment = '{0} = some()'

regular_multiple_assignment = 'result = {0} = some_other_result = some()'

for_assignment = """
def wrapper():
    for {0} in iterable:
        ...
"""

list_comprehension = """
def wrapper():
    comp = [1 for {0} in some()]
"""

generator_expression = """
def wrapper():
    comp = (1 for {0} in some())
"""

set_comprehension = """
def wrapper():
    comp = {{1 for {0} in some()}}
"""

dict_comprehension = """
def wrapper():
    comp = {{'1': 1 for {0} in some()}}
"""

with_assignment = """
def wrapper():
    with some() as {0}:
        ...
"""

with_multiple_assignments = """
def wrapper():
    with some() as s, some_other() as {0} :
        ...
"""


@pytest.mark.parametrize('assignment', [
    list_target,
    spread_assignment_in_list_target,
])
@pytest.mark.parametrize('code', [
    regular_assignment,
    for_assignment,
    list_comprehension,
    generator_expression,
    set_comprehension,
    dict_comprehension,
    with_assignment,
    with_multiple_assignments,
])
def test_unpacking_to_list(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    assignment,
):
    """Ensure that unpacking iterable to list is restricted."""
    tree = parse_ast_tree(code.format(assignment))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnpackingIterableToListViolation])


@pytest.mark.parametrize('assignment', [
    nested_list_target0,
    nested_list_tatget1,
    nested_list_target2,
    multiple_level_nested_list_target,
    nested_spread_assignment_in_list,
    multiple_level_nested_spread_assign_in_list,
])
@pytest.mark.parametrize('code', [
    regular_assignment,
    for_assignment,
    list_comprehension,
    generator_expression,
    set_comprehension,
    dict_comprehension,
    with_assignment,
    with_multiple_assignments,
])
def test_unpacking_to_nested_list(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    assignment,
):
    """Ensure that unpacking iterable to nested list is restricted."""
    tree = parse_ast_tree(code.format(assignment))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [UnpackingIterableToListViolation, WrongUnpackingViolation],
    )


@pytest.mark.parametrize('assignment', [
    list_target,
    nested_list_target0,
    nested_list_tatget1,
    nested_list_target2,
    multiple_level_nested_list_target,
    spread_assignment_in_list_target,
    nested_spread_assignment_in_list,
    multiple_level_nested_spread_assign_in_list,
])
@pytest.mark.parametrize('code', [regular_multiple_assignment])
def test_unpacking_to_list_in_middle_target(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    assignment,
):
    """Ensure that unpacking iterable to list in middle target is restricted."""
    tree = parse_ast_tree(code.format(assignment))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [MultipleAssignmentsViolation, UnpackingIterableToListViolation],
    )

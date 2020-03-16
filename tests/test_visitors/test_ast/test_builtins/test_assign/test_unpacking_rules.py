import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongUnpackingViolation,
)
from wemake_python_styleguide.violations.consistency import (
    IterableUnpackingToListViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import (
    WrongAssignmentVisitor,
)

single_assignment = '{0} = 1'

tuple_assignment1 = 'first, {0} = (1, 2)'
tuple_assignment2 = '{0}, second = (1, 2)'

list_assignment = '[first, second] = (1, 2)'

nested_list_assignment0 = '[first, second], third = ((1, 2), 3)'
nested_list_assignment1 = 'first, [second, third] = (1, (2, 3))'
nested_list_assignment2 = 'first, (second, [third, fourth]) = (1, (2, (3, 4)))'

multiple_level_nested_list_assignment = (
    'first, [second, [third, fourth]] = (1, (2, (3, 4)))'
)

spread_assignment1 = '{0}, *second = [1, 2, 3]'
spread_assignment2 = 'first, *{0} = [1, 2, 3]'

spread_assignment_in_list = '[first, *rest] = [1, 2, 3]'

nested_spread_assignment_in_list = 'first, [second, *rest] = [1, (2, 3, 4)]'

multiple_level_nested_spread_assign_in_list = (
    'first, [second, [*rest, last]] = (1, (2, (3, 4, 5)))'
)

for_assignment = """
def wrapper():
    for {0} in []:
        ...
"""

for_unpacking1 = """
def wrapper():
    for {0}, second in enumerate([]):
        ...
"""

for_unpacking2 = """
def wrapper():
    for first, {0} in enumerate([]):
        ...
"""

list_comprehension = """
def wrapper():
    comp = [1 for first, {0} in enumerate([])]
"""

dict_comprehension = """
def wrapper():
    comp = {{'1': 1 for first, {0} in enumerate([])}}
"""

set_comprehension = """
def wrapper():
    comp = {{1 for {0}, second in enumerate([])}}
"""

generator_expression = """
def wrapper():
    comp = (1 for first, {0} in enumerate([]))
"""

with_assignment = """
def wrapper():
    with some() as {0}:
        ...
"""

with_unpacking1 = """
def wrapper():
    with some() as ({0}, second):
        ...
"""

with_unpacking2 = """
def wrapper():
    with some() as (first, {0}):
        ...
"""


@pytest.mark.parametrize('code', [
    single_assignment,
    tuple_assignment1,
    tuple_assignment2,
    spread_assignment1,
    spread_assignment2,
    for_assignment,
    for_unpacking1,
    for_unpacking2,
    list_comprehension,
    dict_comprehension,
    set_comprehension,
    generator_expression,
    with_assignment,
    with_unpacking1,
    with_unpacking2,
])
def test_correct_unpacking(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that correct assignments work."""
    tree = parse_ast_tree(mode(code.format('some_name')))

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
    mode,
):
    """Testing that correct assignments work."""
    tree = parse_ast_tree(mode(single_assignment.format(assignment)))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    tuple_assignment1,
    tuple_assignment2,
    spread_assignment1,
    spread_assignment2,
    for_unpacking1,
    for_unpacking2,
    list_comprehension,
    dict_comprehension,
    set_comprehension,
    generator_expression,
    with_unpacking1,
    with_unpacking2,
])
@pytest.mark.parametrize('assignment', [
    'some[0]',
    'some["key"]',
    'some[obj]',
    'some.attr',
    'some[0]["key"]',
    'some["key"][0]',
])
def test_multiple_assignments(
    assert_errors,
    parse_ast_tree,
    code,
    assignment,
    default_options,
    mode,
):
    """Testing that multiple assignments are restricted."""
    tree = parse_ast_tree(mode(code.format(assignment)))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongUnpackingViolation])


@pytest.mark.parametrize('code', [
    list_assignment,
    spread_assignment_in_list,
])
def test_unpacking_to_list(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Ensure that unpacking iterable to list is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [IterableUnpackingToListViolation])


@pytest.mark.parametrize('code', [
    nested_list_assignment0,
    nested_list_assignment1,
    nested_list_assignment2,
    nested_spread_assignment_in_list,
])
def test_unpacking_to_nested_list(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Ensure that unpacking iterable to nested list is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [IterableUnpackingToListViolation, WrongUnpackingViolation],
    )


@pytest.mark.parametrize('code', [
    multiple_level_nested_list_assignment,
    multiple_level_nested_spread_assign_in_list,
])
def test_unpacking_to_multiple_level_nested_list(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Test unpacking iterable to multiple levels nested list."""
    tree = parse_ast_tree(code)

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [
            IterableUnpackingToListViolation,
            IterableUnpackingToListViolation,
            WrongUnpackingViolation,
        ],
    )

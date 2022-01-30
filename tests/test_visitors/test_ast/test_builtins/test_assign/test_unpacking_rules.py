import pytest

from wemake_python_styleguide.violations.best_practices import (
    GettingElementByUnpackingViolation,
    SingleElementDestructuringViolation,
    WrongUnpackingViolation,
)
from wemake_python_styleguide.violations.consistency import (
    UnpackingIterableToListViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import (
    WrongAssignmentVisitor,
)

single_assignment = '{0} = 1'
sequence_assignment1 = 'first, {0} = {1}'
sequence_assignment2 = '{0}, second = {1}'
tuple_assignment1 = 'first, {0} = (1, 2)'
tuple_assignment2 = '{0}, second = (1, 2)'

spread_assignment1 = '{0}, *second = [1, 2, 3]'
spread_assignment2 = 'first, *{0} = [1, 2, 3]'
spread_assignment3 = '*{0}, second = [1, 2, 3]'
spread_assignment4 = '(first, second), *{0} = ...'
spread_assignment5 = '*{0}, self.second = [1, 2, 3]'

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

correct_single_destructuring = 'first = {0}'
wrong_single_destructuring1 = 'first, = {0}'
wrong_single_destructuring2 = '(first,) = {0}'
wrong_single_destructuring3 = '[first] = {0}'


@pytest.mark.parametrize('code', [
    single_assignment,
    sequence_assignment1,
    sequence_assignment2,
    tuple_assignment1,
    tuple_assignment2,
    spread_assignment1,
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
@pytest.mark.parametrize('definition', [
    'some_name',
    '(a, b)',  # tuple
])
@pytest.mark.parametrize('target', [
    '(1, 2)',
    '[1, 2]',
])
def test_correct_unpacking(
    assert_errors,
    parse_ast_tree,
    code,
    definition,
    target,
    default_options,
    mode,
):
    """Testing that correct assignments work."""
    tree = parse_ast_tree(mode(code.format(definition, target)))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    spread_assignment2,
])
@pytest.mark.parametrize('definition', [
    'some_name',
])
@pytest.mark.parametrize('target', [
    '(1, 2)',
    '[1, 2]',
])
def test_correct_spread_unpacking(
    assert_errors,
    parse_ast_tree,
    code,
    definition,
    target,
    default_options,
    mode,
):
    """Testing that correct assignments work."""
    tree = parse_ast_tree(mode(code.format(definition, target)))

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
    sequence_assignment1,
    sequence_assignment2,
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
    # regression 1856
    '(some, other[0])',
    '(some.attr, other)',
])
@pytest.mark.parametrize('target', [
    '(1, 2)',
    '[1, 2]',
])
def test_multiple_assignments(
    assert_errors,
    parse_ast_tree,
    code,
    target,
    assignment,
    default_options,
    mode,
):
    """Testing that multiple assignments are restricted."""
    tree = parse_ast_tree(mode(code.format(assignment, target)))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongUnpackingViolation])


@pytest.mark.parametrize('target', [
    '(1,)[0]',
    '[1][0]',
])
def test_correct_destructing(
    assert_errors,
    parse_ast_tree,
    target,
    default_options,
    mode,
):
    """Testing that correct elements destructuring work."""
    tree = parse_ast_tree(mode(correct_single_destructuring.format(target)))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_single_destructuring1,
    wrong_single_destructuring2,
    wrong_single_destructuring3,
])
@pytest.mark.parametrize('assignment', [
    '(1,)',
    '[1]',
    'some',
    'some()',
])
def test_single_element_destructing(
    assert_errors,
    parse_ast_tree,
    code,
    assignment,
    default_options,
    mode,
):
    """Testing that single element destructuring is restricted."""
    tree = parse_ast_tree(mode(code.format(assignment)))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [SingleElementDestructuringViolation],
        ignored_types=UnpackingIterableToListViolation,
    )


@pytest.mark.parametrize('code', [
    spread_assignment2,
    spread_assignment3,
    spread_assignment4,
    spread_assignment5,
])
@pytest.mark.parametrize('definition', [
    '_',
    '_data',
])
def test_element_getting_by_unpacking(
    assert_errors,
    parse_ast_tree,
    code,
    definition,
    default_options,
):
    """Testing that getting element by unpacking is restricted."""
    tree = parse_ast_tree(code.format(definition))

    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [GettingElementByUnpackingViolation],
        ignored_types=WrongUnpackingViolation,
    )

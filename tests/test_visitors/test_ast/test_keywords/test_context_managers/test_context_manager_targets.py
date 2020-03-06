import pytest

from wemake_python_styleguide.violations.consistency import (
    MultipleContextManagerAssignmentsViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    WrongContextManagerVisitor,
)

incorrect_count = """
def wrapper():
    with open('') as first, second:
        ...
"""

incorrect_composite_assign = """
def wrapper():
    with open('first') as first, open('second') as second:
        ...
"""

correct_count = """
def wrapper():
    with open('') as first:
        ...
"""

correct_count_tuple = """
def wrapper():
    with open('') as (first, second):
        ...
"""


@pytest.mark.parametrize('code', [
    incorrect_count,
    incorrect_composite_assign,
])
def test_context_manager_multiple_targets(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing incorrect count context manager assignment."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongContextManagerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MultipleContextManagerAssignmentsViolation])


@pytest.mark.parametrize('code', [
    correct_count,
    correct_count_tuple,
])
def test_context_manager_alone_target(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing correct count context manager assignment."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongContextManagerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

import pytest

from wemake_python_styleguide.violations.best_practices import (
    MultipleVariablesInitializationViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import (
    MultipleVariablesInitializationVisitor,
)

# Correct usages:

function_unpacking = 'first, second = some_tuple()'
swap_assignment = 'first, second = second, first'
single_assignment = 'constant = 1'
spread_assignment = 'first, *_, second = [1, 2, 4, 3]'

# Wrong usages:

tuple_assignment = 'first, second = (1, 2)'
list_unpacking = 'first, second = [], []'
mixed_unpacking = 'first, second = (1, [])'


@pytest.mark.parametrize(
    'code',
    [
        single_assignment,
        spread_assignment,
        function_unpacking,
        swap_assignment,
    ],
)
def test_correct_assignments(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correct assignments work."""
    tree = parse_ast_tree(code)

    visitor = MultipleVariablesInitializationVisitor(
        default_options, tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        tuple_assignment,
        list_unpacking,
        mixed_unpacking,
    ],
)
def test_multiple_variables_initialization(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that multiple variables initialization is restricted."""
    tree = parse_ast_tree(code)

    visitor = MultipleVariablesInitializationVisitor(
        default_options, tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [MultipleVariablesInitializationViolation])

import pytest

from wemake_python_styleguide.violations.best_practices import (
    ApproximateConstantViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import WrongNumberVisitor


@pytest.mark.parametrize('variable_value', [
    # We use string, because these values in numbers raise violations:
    '3.14',
    '3.1415',
    '2.71',
    '2.718',
    '6.28',
    '6.283',
])
def test_violation_on_approximate_constants(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    variable_value,
):
    """Ensures that usage of approximate constants not allowed."""
    tree = parse_ast_tree('my_const = {0}'.format(variable_value))
    visitor = WrongNumberVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ApproximateConstantViolation])
    assert_error_text(visitor, str(variable_value))


@pytest.mark.parametrize('variable_value', [
    3.0,
    3.1,
    3.13,
    3.142,
    3.1416,
    3.15,

    6.2,
    6.3,
    6.29,
    6.284,

    2.7,
    2.717,
    2.7181,
    2.719,
    2.73,

    3,
    2,
    6,
    100,

    '"3.14"',  # strings are allowed
])
def test_no_violations_on_right_constants(
    assert_errors,
    parse_ast_tree,
    default_options,
    variable_value,
):
    """Ensures that usage of simple numbers allowed."""
    tree = parse_ast_tree('a = {0}'.format(variable_value))
    visitor = WrongNumberVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

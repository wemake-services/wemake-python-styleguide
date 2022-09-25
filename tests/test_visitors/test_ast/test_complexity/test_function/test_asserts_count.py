import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyAssertsViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
)

function_without_asserts = 'def function(): ...'

function_with_asserts = """
def function():
    if some:
        assert some()
    assert other(), 'text'
"""

function_with_nested_function_and_asserts = """
def function():  # has two asserts
    def factory():  # has one assert
        assert one()
    assert two()
"""


@pytest.mark.parametrize('code', [
    function_without_asserts,
    function_with_asserts,
    function_with_nested_function_and_asserts,
])
def test_asserts_correct_count(
    assert_errors,
    parse_ast_tree,
    code,
    mode,
    default_options,
):
    """Testing that asserts counted correctly."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_with_asserts,
    function_with_nested_function_and_asserts,
])
def test_asserts_wrong_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    options,
    code,
    mode,
):
    """Testing that many asserts raises a warning."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_asserts=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyAssertsViolation])
    assert_error_text(visitor, '2', option_values.max_asserts)

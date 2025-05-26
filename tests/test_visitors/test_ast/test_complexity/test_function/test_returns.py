import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyReturnsViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
)

function_without_returns = 'def function(): ...'

function_with_returns = """
def function():
    if 1 > 2:
        return 1
    return 0
"""

function_with_nested_function_and_returns = """
def function():  # has one return and a nested function
    def factory():  # has one return
        return 1
    return factory
"""

function_with_nested_class_and_returns = """
def function():  # has one return (we do not count returns in nested objects)
    def inner_function(x):
        return x
    class Factory:
        def method(self):
            return 1
    return inner_function(Factory())
"""


@pytest.mark.parametrize(
    'code',
    [
        function_without_returns,
        function_with_returns,
        function_with_nested_function_and_returns,
        function_with_nested_class_and_returns,
    ],
)
def test_returns_correct_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that returns counted correctly."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        function_with_returns,
    ],
)
def test_returns_wrong_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    options,
    code,
    mode,
):
    """Testing that many returns raises a warning."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_returns=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyReturnsViolation])
    assert_error_text(visitor, '2', option_values.max_returns)


@pytest.mark.parametrize(
    'code',
    [
        function_with_nested_function_and_returns,
        function_with_nested_class_and_returns,
    ],
)
def test_returns_in_nested_objects_correct_count(
    assert_errors,
    parse_ast_tree,
    options,
    code,
    mode,
):
    """Testing that returns in nested functions and classes are not counted."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_returns=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

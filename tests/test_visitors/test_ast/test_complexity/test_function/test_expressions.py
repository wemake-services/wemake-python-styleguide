import pytest

from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
    TooManyExpressionsViolation,
)

function_without_expressions = """
def function():
    return 1
"""

function_with_expressions = """
def function():
    print(1)
    print(2 / 1)
"""

function_with_nested_function_and_expressions = """
def function():
    print(1)

    def factory():
        print(2)
"""


@pytest.mark.parametrize('code', [
    function_without_expressions,
    function_with_expressions,
    function_with_nested_function_and_expressions,
])
def test_expressions_correct_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that expressions counted correctly."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_with_expressions,
    function_with_nested_function_and_expressions,
])
def test_expressions_wrong_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    options,
    code,
    mode,
):
    """Testing that many expressions raises a warning."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_expressions=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyExpressionsViolation])
    assert_error_text(visitor, '2', option_values.max_expressions)

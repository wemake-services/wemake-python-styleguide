import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyArgumentsViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
)

lambda_without_arguments = 'lambda: ...'
lambda_with_single_argument = 'lambda arg1: ...'
lambda_with_default_argument = 'lambda arg1=None: ...'
lambda_with_single_args = 'lambda *args: ...'
lambda_with_posonly_args = 'lambda arg, /: ...'
lambda_with_single_kwargs = 'lambda **kwargs: ...'
lambda_with_single_kwonly = 'lambda *, kwonly=True: ...'


@pytest.mark.parametrize('code', [
    lambda_without_arguments,
    lambda_with_single_argument,
    lambda_with_default_argument,
    lambda_with_single_args,
    lambda_with_posonly_args,
    lambda_with_single_kwargs,
    lambda_with_single_kwonly,
])
def test_correct_arguments_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Ensures that lambda functions with correct argument count works."""
    tree = parse_ast_tree(code)

    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    lambda_without_arguments,
    lambda_with_single_argument,
    lambda_with_default_argument,
    lambda_with_single_args,
    lambda_with_posonly_args,
    lambda_with_single_kwargs,
    lambda_with_single_kwonly,
])
def test_correct_arguments_count_custom_option(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Ensures that lambda functions with correct argument count works."""
    tree = parse_ast_tree(code)

    option_values = options(max_arguments=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    lambda_with_single_argument,
    lambda_with_default_argument,
    lambda_with_single_args,
    lambda_with_posonly_args,
    lambda_with_single_kwargs,
    lambda_with_single_kwonly,
])
def test_no_arguments_error(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    options,
):
    """Ensures that lambda functions with multiple arguments raise an error."""
    tree = parse_ast_tree(code)

    option_values = options(max_arguments=0)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyArgumentsViolation])
    assert_error_text(visitor, '1', option_values.max_arguments)


@pytest.mark.parametrize('code', [
    lambda_without_arguments,
])
def test_no_arguments(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Ensures that lambda functions with no arguments work."""
    tree = parse_ast_tree(code)

    option_values = options(max_arguments=0)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

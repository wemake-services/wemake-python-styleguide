# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
    TooManyArgumentsViolation,
)


# TODO: use `mode` fixture after
# https://github.com/wemake-services/wemake-python-styleguide/issues/308
# will be fixed
def test_correct_arguments_count(
    assert_errors,
    parse_ast_tree,
    single_argument,
    default_options,
):
    """Ensures that functions with correct argument count works."""
    tree = parse_ast_tree(single_argument)

    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_single_argument_count(
    assert_errors,
    parse_ast_tree,
    single_argument,
    options,
):
    """Ensures that functions with correct argument count works."""
    tree = parse_ast_tree(single_argument)

    option_values = options(max_arguments=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_no_arguments(
    assert_errors,
    parse_ast_tree,
    no_arguments,
    options,
):
    """Ensures that functions with no arguments work."""
    tree = parse_ast_tree(no_arguments)

    option_values = options(max_arguments=0)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_single_argument_count_invalid(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    single_argument,
    options,
):
    """Ensures that functions raise violation when there are multiple args."""
    tree = parse_ast_tree(single_argument)

    option_values = options(max_arguments=0)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyArgumentsViolation])
    assert_error_text(visitor, '1')

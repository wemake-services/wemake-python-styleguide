# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
    TooManyArgumentsViolation,
)


def test_correct_arguments_count(
    assert_errors,
    parse_ast_tree,
    single_argument,
    default_options,
    mode,
):
    """Ensures that functions with correct argument count works."""
    tree = parse_ast_tree(mode(single_argument))

    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_single_argument_count(
    assert_errors,
    parse_ast_tree,
    single_argument,
    options,
    mode,
):
    """Ensures that functions with correct argument count works."""
    tree = parse_ast_tree(mode(single_argument))

    option_values = options(max_arguments=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_no_arguments(
    assert_errors,
    parse_ast_tree,
    options,
    mode,
):
    """Ensures that functions with no arguments work."""
    tree = parse_ast_tree(mode('def function(): ...'))

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
    mode,
):
    """Ensures that functions raise violation when there are multiple args."""
    tree = parse_ast_tree(mode(single_argument))

    option_values = options(max_arguments=0)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyArgumentsViolation])
    assert_error_text(visitor, '1')


def test_two_arguments_count_invalid(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    two_arguments,
    options,
    mode,
):
    """Ensures that functions raise violation when there are multiple args."""
    tree = parse_ast_tree(mode(two_arguments))

    option_values = options(max_arguments=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyArgumentsViolation])
    assert_error_text(visitor, '2')

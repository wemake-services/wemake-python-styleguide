from wemake_python_styleguide.violations.naming import TooLongNameViolation
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)

long_name = 'incredibly_long_name_that_should_not_pass_the_long_name_test'


def test_long_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    own_naming_template,
    default_options,
    mode,
):
    """Ensures that long names are not allowed."""
    tree = parse_ast_tree(
        mode(own_naming_template.format(long_name)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongNameViolation])
    assert_error_text(visitor, long_name, default_options.max_name_length)


def test_long_foreign_name(
    assert_errors,
    parse_ast_tree,
    foreign_naming_template,
    default_options,
    mode,
):
    """Ensures that long names are not allowed."""
    tree = parse_ast_tree(
        mode(foreign_naming_template.format(long_name)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_long_variable_name_config(
    assert_errors,
    parse_ast_tree,
    own_naming_template,
    options,
    mode,
):
    """Ensures that it is possible to configure `max_name_length`."""
    long_name = 'incredibly_long_name_that_should_not_pass_the_long_name_test'
    tree = parse_ast_tree(
        mode(own_naming_template.format(long_name)),
    )

    option_values = options(max_name_length=len(long_name) + 1)
    visitor = WrongNameVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

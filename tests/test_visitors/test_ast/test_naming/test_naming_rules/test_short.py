import pytest

from wemake_python_styleguide.violations.naming import (
    TooShortNameViolation,
    TrailingUnderscoreViolation,
)
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)

patterns = (
    'y',
    '_x',
    'z_',
)


@pytest.mark.parametrize('short_name', patterns)
def test_short_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    own_naming_template,
    default_options,
    short_name,
    mode,
):
    """Ensures that short names are not allowed."""
    tree = parse_ast_tree(
        mode(own_naming_template.format(short_name)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [TooShortNameViolation],
        ignored_types=TrailingUnderscoreViolation,
    )
    assert_error_text(
        visitor,
        short_name,
        default_options.min_name_length,
        ignored_types=TrailingUnderscoreViolation,
    )


@pytest.mark.parametrize('short_name', patterns)
def test_short_foreign_name(
    assert_errors,
    parse_ast_tree,
    foreign_naming_template,
    default_options,
    short_name,
    mode,
):
    """Ensures that short names are not allowed."""
    tree = parse_ast_tree(
        mode(foreign_naming_template.format(short_name)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_naming_length_settings(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    own_naming_template,
    options,
    mode,
):
    """Ensures that correct names are allowed."""
    short_name = 'xy'
    tree = parse_ast_tree(
        mode(own_naming_template.format(short_name)),
    )

    option_values = options(min_name_length=3)
    visitor = WrongNameVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooShortNameViolation])
    assert_error_text(visitor, short_name, option_values.min_name_length)

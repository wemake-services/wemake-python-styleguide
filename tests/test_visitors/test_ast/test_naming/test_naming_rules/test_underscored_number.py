import pytest

from wemake_python_styleguide.violations.naming import (
    UnderscoredNumberNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)

patterns = (
    'number_5',
    'between_45_letters',
    'with_multiple_groups_4_5',
)


@pytest.mark.parametrize('number_suffix', patterns)
def test_number_prefix_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    own_naming_template,
    default_options,
    mode,
    number_suffix,
):
    """Ensures that number suffix names are not allowed."""
    tree = parse_ast_tree(
        mode(own_naming_template.format(number_suffix)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnderscoredNumberNameViolation])
    assert_error_text(visitor, number_suffix)


@pytest.mark.parametrize('number_suffix', patterns)
def test_number_prefix_foreign_name(
    assert_errors,
    parse_ast_tree,
    foreign_naming_template,
    default_options,
    mode,
    number_suffix,
):
    """Ensures that number suffix names are not allowed."""
    tree = parse_ast_tree(
        mode(foreign_naming_template.format(number_suffix)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

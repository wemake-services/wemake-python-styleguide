import pytest

from wemake_python_styleguide.violations.naming import (
    ConsecutiveUnderscoresInNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)

patterns = (
    'with__underscore',
    'mutliple__under__score',
    'triple___underscore',
    '__magic__name__',
)


@pytest.mark.parametrize('underscored_name', patterns)
def test_underscored_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    own_naming_template,
    default_options,
    mode,
    underscored_name,
):
    """Ensures that underscored names are not allowed."""
    tree = parse_ast_tree(
        mode(own_naming_template.format(underscored_name)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConsecutiveUnderscoresInNameViolation])
    assert_error_text(visitor, underscored_name)


@pytest.mark.parametrize('underscored_name', patterns)
def test_underscored_attribute_name(
    assert_errors,
    parse_ast_tree,
    foreign_naming_template,
    default_options,
    mode,
    underscored_name,
):
    """Ensures that attribute underscored names are allowed."""
    tree = parse_ast_tree(
        mode(foreign_naming_template.format(underscored_name)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

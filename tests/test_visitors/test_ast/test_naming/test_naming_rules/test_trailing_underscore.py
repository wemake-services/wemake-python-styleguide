import pytest

from wemake_python_styleguide.violations.naming import (
    TrailingUnderscoreViolation,
)
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor


def test_wrong_trailing_underscore(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
):
    """Test names with trailing underscores."""
    wrong_name = 'my_variable_'
    tree = parse_ast_tree(mode(naming_template.format(wrong_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TrailingUnderscoreViolation])
    assert_error_text(visitor, wrong_name)


@pytest.mark.parametrize('correct_name', [
    'list_',
    'class_',
    'async_',
    'await_',
])
def test_correct_trailing_underscore(
    assert_errors,
    parse_ast_tree,
    naming_template,
    default_options,
    correct_name,
    mode,
):
    """Test names with correct trailing underscores."""
    tree = parse_ast_tree(mode(naming_template.format(correct_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

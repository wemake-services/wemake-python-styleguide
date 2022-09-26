import pytest

from wemake_python_styleguide.violations.naming import (
    WrongUnusedVariableNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)


@pytest.mark.parametrize('wrong_name', [
    '__',
    '___',
])
def test_wrong_unused_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
    wrong_name,
):
    """Ensures that wrong names are not allowed."""
    tree = parse_ast_tree(mode(naming_template.format(wrong_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongUnusedVariableNameViolation])
    assert_error_text(visitor, wrong_name)


@pytest.mark.parametrize('wrong_name', [
    '_',
])
def test_correct_unused_variable_name(
    assert_errors,
    parse_ast_tree,
    naming_template,
    skip_match_case_syntax_error,
    default_options,
    mode,
    wrong_name,
):
    """Ensures that wrong names are not allowed."""
    skip_match_case_syntax_error(naming_template, wrong_name)
    tree = parse_ast_tree(mode(naming_template.format(wrong_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

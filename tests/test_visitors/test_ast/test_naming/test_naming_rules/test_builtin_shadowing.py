import pytest

from wemake_python_styleguide.constants import BUILTINS_WHITELIST
from wemake_python_styleguide.violations.naming import BuiltinShadowingViolation
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)

real_builtins = frozenset((
    'list',
    'str',
    'sum',
))


@pytest.mark.parametrize('wrong_name', real_builtins)
def test_builtin_shadowing(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    non_attribute_template,
    default_options,
    mode,
    wrong_name,
):
    """Test names that shadow builtins."""
    tree = parse_ast_tree(
        mode(non_attribute_template.format(wrong_name)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BuiltinShadowingViolation])
    assert_error_text(visitor, wrong_name)


@pytest.mark.parametrize('wrong_name', BUILTINS_WHITELIST)
def test_builtin_shadowing_whitelist(
    assert_errors,
    parse_ast_tree,
    non_attribute_template,
    skip_match_case_syntax_error,
    default_options,
    mode,
    wrong_name,
):
    """Test names that shadow allowed builtins."""
    skip_match_case_syntax_error(non_attribute_template, wrong_name)
    tree = parse_ast_tree(
        mode(non_attribute_template.format(wrong_name)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('wrong_name', real_builtins | BUILTINS_WHITELIST)
def test_builtin_attribute(
    assert_errors,
    parse_ast_tree,
    attribute_template,
    default_options,
    mode,
    wrong_name,
):
    """Test attribute names that do not shadow builtins."""
    tree = parse_ast_tree(
        mode(attribute_template.format(wrong_name)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

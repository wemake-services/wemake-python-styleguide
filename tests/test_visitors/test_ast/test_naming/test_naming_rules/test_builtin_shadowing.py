import pytest

from wemake_python_styleguide.violations.naming import BuiltinShadowingViolation
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)


@pytest.mark.parametrize('wrong_name', [
    'list',
    'str',
    'sum',
])
def test_builtin_shadowing(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
    wrong_name,
):
    """Test names that shadow builtins."""
    tree = parse_ast_tree(mode(naming_template.format(wrong_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BuiltinShadowingViolation])
    assert_error_text(visitor, wrong_name)

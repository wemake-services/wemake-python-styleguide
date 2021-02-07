import pytest

from wemake_python_styleguide.violations.naming import (
    ConsecutiveUnderscoresInNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)


@pytest.mark.parametrize('underscored_name', [
    'with__underscore',
    'mutliple__under__score',
    'triple___underscore',
    '__magic__name__',
])
def test_underscored_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
    underscored_name,
):
    """Ensures that underscored names are not allowed."""
    tree = parse_ast_tree(mode(naming_template.format(underscored_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConsecutiveUnderscoresInNameViolation])
    assert_error_text(visitor, underscored_name)

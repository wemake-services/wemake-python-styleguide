import pytest

from wemake_python_styleguide.violations.naming import UnicodeNameViolation
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)


@pytest.mark.parametrize('wrong_name', [
    'тестовое_имя',
    'test_имя2',
    'сос',  # written with identical to ASCII russian chars
    'some_變量',
])
def test_wrong_unicode(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
    wrong_name,
):
    """Test names with unicode."""
    tree = parse_ast_tree(mode(naming_template.format(wrong_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnicodeNameViolation])
    assert_error_text(visitor, wrong_name)

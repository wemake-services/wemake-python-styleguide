# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import UnicodeNameViolation
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor

wrong_unicode_full_unicode_name = 'тестовое_имя'

wrong_unicode_part_unicode_name = 'test_имя'


@pytest.mark.parametrize('wrong_name', [
    wrong_unicode_full_unicode_name,
    wrong_unicode_part_unicode_name,
])
def test_function_unicode(
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

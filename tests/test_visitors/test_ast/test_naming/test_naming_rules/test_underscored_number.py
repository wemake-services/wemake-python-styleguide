# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import (
    UnderscoredNumberNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor


@pytest.mark.parametrize('number_suffix', [
    'number_5',
    'between_45_letters',
    'with_multiple_groups_4_5',
])
def test_number_prefix_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
    number_suffix,
):
    """Ensures that number suffix names are not allowed."""
    tree = parse_ast_tree(mode(naming_template.format(number_suffix)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnderscoredNumberNameViolation])
    assert_error_text(visitor, number_suffix)

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor


@pytest.mark.parametrize('correct_name', [
    'snake_case',
    '_protected_or_unused',
    'with_number5',
])
def test_naming_correct(
    assert_errors,
    parse_ast_tree,
    naming_template,
    options,
    correct_name,
):
    """Ensures that correct names are allowed."""
    tree = parse_ast_tree(naming_template.format(correct_name))

    option_values = options(min_name_length=3)
    visitor = WrongNameVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

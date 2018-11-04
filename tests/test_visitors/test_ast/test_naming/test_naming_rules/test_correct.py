# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor


@pytest.mark.parametrize('correct_name', [
    'snake_case',
    '_protected_or_unused',
    'with_number5',
    'xy',
])
def test_naming_correct(
    assert_errors,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
    correct_name,
):
    """Ensures that correct names are allowed."""
    tree = parse_ast_tree(mode(naming_template.format(correct_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

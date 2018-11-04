# -*- coding: utf-8 -*-

from wemake_python_styleguide.violations.naming import PrivateNameViolation
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor


def test_private_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
):
    """Ensures that private names are not allowed."""
    private_name = '__private'
    tree = parse_ast_tree(mode(naming_template.format(private_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [PrivateNameViolation])
    assert_error_text(visitor, private_name)

# -*- coding: utf-8 -*-

from wemake_python_styleguide.violations.naming import TooLongNameViolation
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor


def test_long_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
):
    """Ensures that short names are not allowed."""
    long_name = 'incredibly_long_name_that_should_not_pass_the_long_name_test'
    tree = parse_ast_tree(mode(naming_template.format(long_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongNameViolation])
    assert_error_text(visitor, long_name)

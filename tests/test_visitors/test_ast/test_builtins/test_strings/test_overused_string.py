# -*- coding: utf-8 -*-

from wemake_python_styleguide.violations.complexity import (
    OverusedStringViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import WrongStringVisitor

string_actions = """
first = {0}
second({0})
third[{0}]
'new' + {0}
"""

string_values = ['"same-string"', "''"]


def test_string_overuse_settings(
    assert_errors,
    parse_ast_tree,
    options,
):
    """Ensures that settings for string over-use work."""
    tree = parse_ast_tree(string_actions.format('"same-string"'))

    option_values = options(max_string_usages=4)
    visitor = WrongStringVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_string_overuse(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
):
    """Ensures that over-used strings raise violations."""
    for string_val in string_values:
        tree = parse_ast_tree(string_actions.format(string_val))

        visitor = WrongStringVisitor(default_options, tree=tree)
        visitor.run()

        assert_errors(visitor, [OverusedStringViolation])
        assert_error_text(visitor, string_val.replace('"', ''))

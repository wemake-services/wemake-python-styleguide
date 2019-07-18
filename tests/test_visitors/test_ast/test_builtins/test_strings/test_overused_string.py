# -*- coding: utf-8 -*-

import pytest

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


@pytest.mark.parametrize('strings', [
    string_actions,
])
@pytest.mark.parametrize('string_value', ['"same_string"'])
def test_string_overuse_settings(
    assert_errors,
    parse_ast_tree,
    options,
    strings,
    string_value,
):
    """Ensures that settings for string over-use work."""
    tree = parse_ast_tree(strings.format(string_value))

    option_values = options(max_string_usages=4)
    visitor = WrongStringVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('strings', [
    string_actions,
])
@pytest.mark.parametrize('string_value', [
    '"same-string"',
    "''",
])
def test_string_overuse(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    strings,
    string_value,
):
    """Ensures that over-used strings raise violations."""
    tree = parse_ast_tree(strings.format(string_value))

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [OverusedStringViolation])
    assert_error_text(visitor, string_value.replace('"', ''))

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

string_function_type_annotations = """
def first(
    arg1: {0},
    arg2: {0},
    arg3: {0},
) -> {0}:
    ...
"""

string_class_type_annotations = """
class SomeClass(object):
    first: {0}
    second: {0}
    third: {0}
    fourth: {0}
"""

string_method_type_annotations = """
class SomeClass(object):
    def first(
        self,
        arg1: {0},
        arg2: {0},
        arg3: {0},
    ) -> {0}:
        ...
"""

string_variable_type_annotations = """
first: {0}
second: {0}
third: {0}
fourth: {0}
"""


@pytest.mark.parametrize('strings', [
    string_actions,
    string_function_type_annotations,
    string_class_type_annotations,
    string_method_type_annotations,
    string_variable_type_annotations,
])
@pytest.mark.parametrize('string_value', [
    '"same_string"',
    '"GenericType[int, str]"',
])
def test_string_overuse_settings(
    assert_errors,
    parse_ast_tree,
    options,
    strings,
    string_value,
    mode,
):
    """Ensures that settings for string over-use work."""
    tree = parse_ast_tree(mode(strings.format(string_value)))

    option_values = options(max_string_usages=4)
    visitor = WrongStringVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('strings', [
    string_actions,
])
@pytest.mark.parametrize('string_value', [
    '"same-string"',
    '"GenericType[int, str]"',
    "''",
    '""',
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
    assert_error_text(visitor, string_value.replace('"', '') or "''")


@pytest.mark.parametrize('strings', [
    string_function_type_annotations,
    string_class_type_annotations,
    string_method_type_annotations,
    string_variable_type_annotations,
])
@pytest.mark.parametrize('string_value', [
    '"GenericType[int, str]"',
    '"int"',
])
def test_string_type_annotations(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    options,
    strings,
    string_value,
    mode,
):
    """Ensures that type annotations do not raise violations."""
    tree = parse_ast_tree(mode(strings.format(string_value)))

    option_values = options(max_string_usages=0)
    visitor = WrongStringVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

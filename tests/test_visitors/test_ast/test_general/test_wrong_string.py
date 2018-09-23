# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.general.wrong_string import (
    FormattedStringViolation,
    WrongStringVisitor,
)

regular_string = "'some value'"
string_variable = "some = '123'"
formated_string = "'x + y = {0}'.format(2)"
key_formated_string = "'x + y = {res}'.format(res=2)"
variable_format = """
some = 'x = {0}'
some.format(2)
"""

f_string = "f'x + y = {2 + 2}'"
f_empty_string = "f''"


@pytest.mark.parametrize('code', [
    regular_string,
    string_variable,
    formated_string,
    key_formated_string,
    variable_format,
])
def test_string_normal(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that regular strings work well."""
    tree = parse_ast_tree(code)

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    f_string,
    f_empty_string,
])
def test_wrong_string(assert_errors, parse_ast_tree, code, default_options):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [FormattedStringViolation])

import pytest

from wemake_python_styleguide.violations.complexity import (
    TooComplexFormattedStringViolation,
)
from wemake_python_styleguide.violations.consistency import (
    FormattedStringViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import WrongStringVisitor

regular_string = "'some value'"
binary_string = "b'binary'"
unicode_string = "u'unicode'"
string_variable = "some = '123'"
formated_string = "'x + y = {0}'.format(2)"
key_formated_string = "'x + y = {res}'.format(res=2)"
variable_format = """
some = 'x = {0}'
some.format(2)
"""

f_string = "f'x + y = {2 + 2}'"
f_empty_string = "f''"
f_complex_f_string = """
    f'{reverse(\"url-name\")}?{\"&\".join(\"user=\"+uid for uid in user_ids)}'
"""
f_variable_lookup = "f'smth {value}'"
f_dict_lookup_str_key = "f'smth {dict_value[\"key\"]}'"
f_list_index_lookup = "f'smth {list_value[0]}'"
f_function_empty_args = "f'smth {user.get_full_name()}'"
f_function_with_args = "f'smth {func(arg)}'"
f_dict_lookup_function_empty_args = "f'smth {dict_value[func()]}'"
f_list_slice_lookup = "f'smth {list[:]}'"


@pytest.mark.parametrize('code', [
    regular_string,
    binary_string,
    unicode_string,
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
    f_empty_string,
])
def test_wrong_string(assert_errors, parse_ast_tree, code, default_options):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [FormattedStringViolation])


@pytest.mark.parametrize('code', [
    f_complex_f_string,
    f_function_with_args,
    f_dict_lookup_function_empty_args,
    f_string,
    f_list_slice_lookup,
])
def test_complex_f_string(assert_errors, parse_ast_tree, code, default_options):
    """Testing that ..."""
    tree = parse_ast_tree(code)

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        FormattedStringViolation,
        TooComplexFormattedStringViolation,
    ])


@pytest.mark.parametrize('code', [
    f_dict_lookup_str_key,
    f_function_empty_args,
    f_list_index_lookup,
    f_variable_lookup,
])
def test_simple_f_string(assert_errors, parse_ast_tree, code, default_options):
    """Testing that ..."""
    tree = parse_ast_tree(code)

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [FormattedStringViolation])

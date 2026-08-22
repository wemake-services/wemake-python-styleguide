import pytest

from wemake_python_styleguide.compat.constants import PY314
from wemake_python_styleguide.violations.complexity import (
    TooComplexFormattedStringViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import (
    WrongFormatStringVisitor,
    WrongStringVisitor,
)

regular_string = "'some value'"
binary_string = "b'binary'"
unicode_string = "u'unicode'"
string_variable = "some = '123'"
formatted_string = "'x + y = {0}'.format(2)"
key_formatted_string = "'x + y = {res}'.format(res=2)"
variable_format = """
some = 'x = {0}'
some.format(2)
"""

# Allowed
f_single_chained_attr = "{0}'{{attr1.attr2}}'"
f_variable_lookup = "{0}'smth {{value}}'"
f_multi_variable_lookup = "{0}'smth {{value1}} {{value2}} {{value3}}'"
f_dict_lookup_str_key = '{0}\'smth {{dict_value["key"]}}\''
f_list_index_lookup = "{0}'smth {{list_value[0]}}'"
f_function_empty_args = "{0}'smth {{user.get_full_name()}}'"
f_attr_on_function = "{0}'{{fcn().attr}}'"
f_true_index = "{0}'{{array[True]}}'"
f_none_index = "{0}'{{array[None]}}'"
f_byte_index = '{0}\'{{array[b"Hello"]}}\''
f_empty_string = "{0}''"
f_function_with_single_arg = "{0}'smth {{func(arg)}}'"
f_function_with_three_args = "{0}'{{func(arg1, arg2, arg3)}}'"
f_method_with_three_args = "{0}'{{obj.method(arg1, arg2, arg3)}}'"
f_assign = "{0}'{{value=}}'"
f_assign_attr = "{0}'{{value.attr=}}'"
f_assign_call = "{0}'{{value()=}}'"

# Allowed format specifiers
f_format_aligned = "{0}'{{value:<5}}'"
f_format_str = "{0}'{{value!s}}'"
f_format_repr = "{0}'{{value!r}}'"
f_format_code = "{0}'{{value!a}}'"
f_format_hex_lower_short = "{0}'{{value:x}}'"
f_format_hex_upper_short = "{0}'{{value:X}}'"
f_format_hex_lower_long = "{0}'{{value:#x}}'"
f_format_hex_upper_long = "{0}'{{value:#X}}'"
f_format_char = "{0}'{{value:c}}'"
f_format_rounded = "{0}'{{value:.123456f}}'"
f_format_scientific = "{0}'{{value:.456789e}}'"
f_format_var_single = "{0}'{{value:{{fmt}}}}'"
f_format_var_single2 = "{0}'{{value1:{{fmt1}}}} {{value2:{{fmt2}}}}'"
f_format_var_single_index = "{0}'{{value:{{fmt[0]}}}}'"
f_format_var_single_call = "{0}'{{value:{{fmt()}}}}'"
f_format_conversions = "{0}'{{value1!r}} {{value2!s}} {{value3!a}}'"
f_format_assign = "{0}'{{value=:<8}}'"
f_format_assign_conversion = "{0}'{{value=!r}}'"
f_format_assign_attr = "{0}'{{value.attr=:.456e}}'"
f_format_assign_var_single = "{0}'{{value=:{{fmt}}}}'"
f_format_assign_var_single2 = "{0}'{{value1=:{{fmt1}}}} {{value2=:{{fmt2}}}}'"

# Disallowed
f_string = "{0}'x + y = {{2 + 2}}'"
f_double_indexing = "{0}'{{list[0][1]}}'"
f_calling_returned_function = "{0}'{{calling_returned_function()()}}'"
f_complex_f_string = """
    {0}'{{reverse("url-name")}}?{{"&".join("user=" + uid for uid in user_ids)}}'
"""
f_dict_lookup_function_empty_args = "{0}'smth {{dict_value[func()]}}'"
f_list_slice_lookup = "{0}'smth {{list[:]}}'"
f_attr_on_returned_value = "{0}'{{some.call().attr}}'"
f_function_on_attr = "{0}'{{some.attr.call()}}'"
f_array_object = "{0}'{{some.first[0].attr.other}}'"
f_double_chained_attr = "{0}'{{attr1.attr2.attr3}}'"
f_triple_call = "{0}'{{foo()()()}}'"
f_triple_lookup = "{0}'{{arr[0][1][2]}}'"
f_double_call_arg = "{0}'{{foo()(arg)}}'"
f_single_chained_functions = "{0}'{{f1().f2()}}'"
f_function_with_four_args = "{0}'{{func(arg1, arg2, arg3, arg4)}}'"
f_method_with_four_args = "{0}'{{obj.meth(arg1, arg2, arg3, arg4)}}-post'"
f_nested_string = """{0}'{{{0}"{{value}}"}}'"""  # noqa: WPS322
# Disallowed format specifiers
f_format_var_multi = "{0}'pre {{value:{{fmt1}}{{fmt2}}}}'"
f_format_var_chain = "{0}'{{value:{{fmt.attr.attr}}}}'"
f_format_var_before1 = "{0}'{{value:{{fmt}}10}}'"
f_format_var_before2 = "{0}'{{value:{{fmt}}.4f}}'"
f_format_var_after1 = "{0}'{{value:_{{fmt}}}}'"
f_format_var_after2 = "{0}'{{value:_^{{fmt}}}}'"
f_format_var_between1 = "{0}'{{value:_{{fmt}}10}}'"
f_format_var_between2 = "{0}'{{value:.{{precision}}f}}'"
f_format_var_around = "{0}'{{value:{{fmt1}}^{{fmt2}}}}'"
f_format_str_const = "{0}'{{value!s:10}}'"
f_format_repr_const = "{0}'{{value!r:10}}'"
f_format_code_const = "{0}'{{value!a:10}}'"
f_format_str_var = "{0}'{{value!s:{{fmt}}}}'"
f_format_repr_var = "{0}'{{value!r:{{fmt}}}}'"
f_format_code_var = "{0}'{{value!a:{{fmt}}}}'"
f_format_hex_lower_short_const = "{0}'{{value:10x}}'"
f_format_hex_upper_short_const = "{0}'{{value:10X}}'"
f_format_hex_lower_long_const = "{0}'{{value:#10x}}'"
f_format_hex_upper_long_const = "{0}'{{value:#10X}}'"
f_format_char_const = "{0}'{{value:10c}}'"
f_format_round_const = "{0}'{{value:10.4f}}'"
f_format_scientific_const = "{0}'{{value:10.7e}}'"
f_format_useless1 = "{0}'{{value:_}}'"
f_format_useless2 = "{0}'{{value:_<}}'"
f_format_assign_const = "{0}'{{value=:_^8.2f}}'"
f_format_assign_conversion_const = "{0}'{{value=!r:_>11}}'"
f_format_assign_var_chain = "{0}'{{value=:{{fmt.attr.attr}}}}'"
f_format_assign_var_multi = "{0}'{{value=:{{fmt1}}{{fmt2}}}}'"

# regression 1921
f_string_comma_format = '{0}"Count={{count:,}}"'

PREFIXES = (
    'f',
    pytest.param(
        't',
        marks=pytest.mark.skipif(
            not PY314,
            reason='t-strings are only in Python 3.14+',
        ),
    ),
)


@pytest.mark.parametrize(
    'code',
    [
        regular_string,
        binary_string,
        unicode_string,
        string_variable,
        formatted_string,
        key_formatted_string,
        variable_format,
    ],
)
def test_string_normal(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that regular strings work well."""
    tree = parse_ast_tree(code)

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('prefix', PREFIXES)
@pytest.mark.parametrize(
    'code',
    [
        f_complex_f_string,
        f_dict_lookup_function_empty_args,
        f_string,
        f_list_slice_lookup,
        f_attr_on_returned_value,
        f_function_on_attr,
        f_array_object,
        f_double_chained_attr,
        f_triple_call,
        f_triple_lookup,
        f_double_call_arg,
        f_double_indexing,
        f_calling_returned_function,
        f_single_chained_functions,
        f_function_with_four_args,
        f_method_with_four_args,
        f_nested_string,
        # format specifiers
        f_format_var_multi,
        f_format_var_chain,
        f_format_var_before1,
        f_format_var_before2,
        f_format_var_after1,
        f_format_var_after2,
        f_format_var_between1,
        f_format_var_between2,
        f_format_var_around,
        f_format_str_const,
        f_format_repr_const,
        f_format_code_const,
        f_format_str_var,
        f_format_repr_var,
        f_format_code_var,
        f_format_hex_lower_short_const,
        f_format_hex_upper_short_const,
        f_format_hex_lower_long_const,
        f_format_hex_upper_long_const,
        f_format_char_const,
        f_format_round_const,
        f_format_scientific_const,
        f_format_useless1,
        f_format_useless2,
        f_format_assign_const,
        f_format_assign_conversion_const,
        f_format_assign_var_chain,
        f_format_assign_var_multi,
    ],
)
def test_complex_formatted_string(
    assert_errors,
    parse_ast_tree,
    code,
    prefix,
    default_options,
):
    """Testing that complex formatted strings are not allowed."""
    tree = parse_ast_tree(code.format(prefix))

    visitor = WrongFormatStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [TooComplexFormattedStringViolation],
    )


@pytest.mark.parametrize('prefix', PREFIXES)
@pytest.mark.parametrize(
    'code',
    [
        f_dict_lookup_str_key,
        f_function_empty_args,
        f_list_index_lookup,
        f_variable_lookup,
        f_multi_variable_lookup,
        f_single_chained_attr,
        f_attr_on_function,
        f_true_index,
        f_none_index,
        f_byte_index,
        f_string_comma_format,
        f_empty_string,
        f_function_with_single_arg,
        f_function_with_three_args,
        f_method_with_three_args,
        f_assign,
        f_assign_attr,
        f_assign_call,
        # format specifiers
        f_format_aligned,
        f_format_str,
        f_format_repr,
        f_format_code,
        f_format_hex_lower_short,
        f_format_hex_upper_short,
        f_format_hex_lower_long,
        f_format_hex_upper_long,
        f_format_char,
        f_format_rounded,
        f_format_scientific,
        f_format_var_single,
        f_format_var_single2,
        f_format_var_single_index,
        f_format_var_single_call,
        f_format_conversions,
        f_format_assign,
        f_format_assign_conversion,
        f_format_assign_attr,
        f_format_assign_var_single,
        f_format_assign_var_single2,
    ],
)
def test_simple_formatted_string(
    assert_errors,
    parse_ast_tree,
    code,
    prefix,
    default_options,
):
    """Testing that non complex formatted strings are allowed."""
    tree = parse_ast_tree(code.format(prefix))

    visitor = WrongFormatStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

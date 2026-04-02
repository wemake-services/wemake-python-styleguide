import pytest

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
f_single_chained_attr = "f'{attr1.attr2}'"
f_variable_lookup = "f'smth {value}'"
f_multi_variable_lookup = "f'smth {value1} {value2} {value3}'"
f_dict_lookup_str_key = 'f\'smth {dict_value["key"]}\''
f_list_index_lookup = "f'smth {list_value[0]}'"
f_function_empty_args = "f'smth {user.get_full_name()}'"
f_attr_on_function = "f'{fcn().attr}'"
f_true_index = "f'{array[True]}'"
f_none_index = "f'{array[None]}'"
f_byte_index = 'f\'{array[b"Hello"]}\''
f_empty_string = "f''"
f_function_with_single_arg = "f'smth {func(arg)}'"
f_function_with_three_args = "f'{func(arg1, arg2, arg3)}'"
f_method_with_three_args = "f'{obj.method(arg1, arg2, arg3)}'"
f_assign = "f'{value=}'"
f_assign_attr = "f'{value.attr=}'"
f_assign_call = "f'{value()=}'"

# Allowed format specifiers
f_format_aligned = "f'{value:<5}'"
f_format_str = "f'{value!s}'"
f_format_repr = "f'{value!r}'"
f_format_code = "f'{value!a}'"
f_format_hex_lower_short = "f'{value:x}'"
f_format_hex_upper_short = "f'{value:X}'"
f_format_hex_lower_long = "f'{value:#x}'"
f_format_hex_upper_long = "f'{value:#X}'"
f_format_char = "f'{value:c}'"
f_format_rounded = "f'{value:.123456f}'"
f_format_scientific = "f'{value:.456789e}'"
f_format_var_single = "f'{value:{fmt}}'"
f_format_var_single2 = "f'{value1:{fmt1}} {value2:{fmt2}}'"
f_format_var_single_index = "f'{value:{fmt[0]}}'"
f_format_var_single_call = "f'{value:{fmt()}}'"
f_format_conversions = "f'{value1!r} {value2!s} {value3!a}'"
f_format_assign = "f'{value=:<8}'"
f_format_assign_conversion = "f'{value=!r}'"
f_format_assign_attr = "f'{value.attr=:.456e}'"
f_format_assign_var_single = "f'{value=:{fmt}}'"
f_format_assign_var_single2 = "f'{value1=:{fmt1}} {value2=:{fmt2}}'"

# Disallowed
f_string = "f'x + y = {2 + 2}'"
f_double_indexing = "f'{list[0][1]}'"
f_calling_returned_function = "f'{calling_returned_function()()}'"
f_complex_f_string = """
    f'{reverse(\"url-name\")}?{\"&\".join(\"user=\"+uid for uid in user_ids)}'
"""
f_dict_lookup_function_empty_args = "f'smth {dict_value[func()]}'"
f_list_slice_lookup = "f'smth {list[:]}'"
f_attr_on_returned_value = "f'{some.call().attr}'"
f_function_on_attr = "f'{some.attr.call()}'"
f_array_object = "f'{some.first[0].attr.other}'"
f_double_chained_attr = "f'{attr1.attr2.attr3}'"
f_triple_call = "f'{foo()()()}'"
f_triple_lookup = "f'{arr[0][1][2]}'"
f_double_call_arg = "f'{foo()(arg)}'"
f_single_chained_functions = "f'{f1().f2()}'"
f_function_with_four_args = "f'{func(arg1, arg2, arg3, arg4)}'"
f_method_with_four_args = "f'{obj.meth(arg1, arg2, arg3, arg4)}-post'"
f_nested_string = 'f\'{f"{value}"}\''
# Disallowed format specifiers
f_format_var_multi = "f'pre {value:{fmt1}{fmt2}}'"
f_format_var_chain = "f'{value:{fmt.attr.attr}}'"
f_format_var_before1 = "f'{value:{fmt}10}'"
f_format_var_before2 = "f'{value:{fmt}.4f}'"
f_format_var_after1 = "f'{value:_{fmt}}'"
f_format_var_after2 = "f'{value:_^{fmt}}'"
f_format_var_between1 = "f'{value:_{fmt}10}'"
f_format_var_between2 = "f'{value:.{precision}f}'"
f_format_var_around = "f'{value:{fmt1}^{fmt2}}'"
f_format_str_const = "f'{value!s:10}'"
f_format_repr_const = "f'{value!r:10}'"
f_format_code_const = "f'{value!a:10}'"
f_format_str_var = "f'{value!s:{fmt}}'"
f_format_repr_var = "f'{value!r:{fmt}}'"
f_format_code_var = "f'{value!a:{fmt}}'"
f_format_hex_lower_short_const = "f'{value:10x}'"
f_format_hex_upper_short_const = "f'{value:10X}'"
f_format_hex_lower_long_const = "f'{value:#10x}'"
f_format_hex_upper_long_const = "f'{value:#10X}'"
f_format_char_const = "f'{value:10c}'"
f_format_round_const = "f'{value:10.4f}'"
f_format_scientific_const = "f'{value:10.7e}'"
f_format_useless1 = "f'{value:_}'"
f_format_useless2 = "f'{value:_<}'"
f_format_assign_const = "f'{value=:_^8.2f}'"
f_format_assign_conversion_const = "f'{value=!r:_>11}'"
f_format_assign_var_chain = "f'{value=:{fmt.attr.attr}}'"
f_format_assign_var_multi = "f'{value=:{fmt1}{fmt2}}'"

# regression 1921
f_string_comma_format = 'f"Count={count:,}"'


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
def test_complex_f_string(assert_errors, parse_ast_tree, code, default_options):
    """Testing that complex ``f`` strings are not allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongFormatStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [TooComplexFormattedStringViolation],
    )


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
def test_simple_f_string(assert_errors, parse_ast_tree, code, default_options):
    """Testing that non complex ``f`` strings are allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongFormatStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import MAGIC_NUMBERS_WHITELIST
from wemake_python_styleguide.violations.best_practices import (
    MagicNumberViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import MagicNumberVisitor

# Correct usages:

assignment = 'constant = {0}'
assignment_unary = 'constant = -{0}'

function_definition = """
def function_name(param1, param2={0}):
    return param1 / param2
"""

list_definition = '[{0}]'
dict_definition_key = '{{{0}: "value"}}'
dict_definition_value = '{{"first": {0}}}'
set_definition = '{{"first", {0}, "other"}}'
tuple_definition = '({0}, )'

# Incorrect usages:

assignment_binop = 'final = {0} + 1'
function_call = 'print({0})'
function_call_named = 'print(end={0})'
expression = '{0}'

inside_function = """
def wrapper():
    some_value = called_func() * {0}
"""

inside_class = """
class Test(object):
    class_field = SOME_CONST - {0}
"""

inside_method = """
class Test(object):
    def method(self):
        return {0}
"""

list_index = """
some_list = [10, 20, 30]
some_list[{0}]
"""

dict_key = """
some_dict = {{11: 12, 13: 14}}
some_dict[{0}]
"""


@pytest.mark.parametrize('code', [
    assignment,
    assignment_unary,
    function_definition,
    list_definition,
    dict_definition_key,
    dict_definition_value,
    set_definition,
    tuple_definition,
])
@pytest.mark.parametrize('number', [
    -10,
    -1,
    0,
    0.5,
    8.3,
    10,
    765,
    '0x20',
    '0o12',
])
def test_magic_number(
    assert_errors,
    parse_ast_tree,
    code,
    number,
    default_options,
    mode,
):
    """Testing that there are no magic numbers in this code."""
    tree = parse_ast_tree(mode(code.format(number)))

    visitor = MagicNumberVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    assignment_binop,
    function_call,
    function_call_named,
    expression,
    inside_function,
    inside_class,
    inside_method,
    list_index,
    dict_key,
])
@pytest.mark.parametrize('number', [
    *MAGIC_NUMBERS_WHITELIST,
    0,
    1,
    5,
    10,
])
def test_magic_number_whitelist(
    assert_errors,
    parse_ast_tree,
    code,
    number,
    default_options,
    mode,
):
    """Testing that magic numbers in this code are whitelisted."""
    tree = parse_ast_tree(mode(code.format(number)))

    visitor = MagicNumberVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    assignment_binop,
    function_call,
    function_call_named,
    expression,
    inside_function,
    inside_class,
    inside_method,
    list_index,
    dict_key,
])
@pytest.mark.parametrize('number', [
    '-0.3',
    '999',
    '10.0',
    '0.0',
    '--134',
    '8.3',
])
def test_magic_number_warning(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    number,
    default_options,
    mode,
):
    """Testing that magic numbers in this code are warnings."""
    tree = parse_ast_tree(mode(code.format(number)))

    visitor = MagicNumberVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MagicNumberViolation])
    assert_error_text(visitor, number.replace('-', ''))


@pytest.mark.parametrize('code', [
    assignment_binop,
    function_call,
    function_call_named,
    expression,
    inside_function,
    inside_class,
    inside_method,
    list_index,
    dict_key,
])
@pytest.mark.parametrize('number', [
    '0b1111',
    '0x20',
    '-0o15',
])
def test_magic_number_octal_warning(
    assert_errors,
    parse_ast_tree,
    code,
    number,
    default_options,
    mode,
):
    """Testing that magic numbers in this code are warnings."""
    tree = parse_ast_tree(mode(code.format(number)))

    visitor = MagicNumberVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MagicNumberViolation])

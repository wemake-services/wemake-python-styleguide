# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.errors.best_practices import MagicNumberViolation
from wemake_python_styleguide.visitors.ast.complexity.numbers import (
    MAGIC_NUMBERS_WHITELIST,
    MagicNumberVisitor,
)

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
expression = '{0}'

list_index = """
some_list = [1, 2, 3]
some_list[{0}]
"""

dict_key = """
some_dict = {{1: 1, 2: 2}}
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
    1000,
])
def test_magic_number(
    assert_errors,
    parse_ast_tree,
    code,
    number,
    default_options,
):
    """Testing that there are no magic numbers in this code."""
    tree = parse_ast_tree(code.format(number))

    visitor = MagicNumberVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    assignment_binop,
    function_call,
    expression,
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
):
    """Testing that magic numbers in this code are whitelisted."""
    tree = parse_ast_tree(code.format(number))

    visitor = MagicNumberVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    assignment_binop,
    function_call,
    expression,
    list_index,
    dict_key,
])
@pytest.mark.parametrize('number', [
    -0.3,
    999,
    10.0,
    0.0,
    -134,
])
def test_magic_number_warning(
    assert_errors,
    parse_ast_tree,
    code,
    number,
    default_options,
):
    """Testing that magic numbers in this code are warnings."""
    tree = parse_ast_tree(code.format(number))

    visitor = MagicNumberVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MagicNumberViolation])

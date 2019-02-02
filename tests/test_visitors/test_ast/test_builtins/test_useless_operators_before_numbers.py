# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.builtins import (
    UselessOperatorsVisitor,
)
from wemake_python_styleguide.violations.consistency import (
    UselessOperatorsViolation,
)

# Usages:
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

usages = [
    assignment,
    assignment_unary,
    function_definition,
    list_definition,
    dict_definition_key,
    dict_definition_value,
    set_definition,
    tuple_definition,
]


@pytest.mark.parametrize('code', usages)
@pytest.mark.parametrize('number', [
   '+5',
   '+0.5',
   '+0x20',
   '+0o12',
   '++5',
   '-+5',
   '~+8',
])
def test_plus_sign_before_numbers(
    assert_errors,
    parse_ast_tree,
    code,
    number,
    default_options,
    mode,
):
    """Testing that there is no useless plus sign before a number."""
    tree = parse_ast_tree(mode(code.format(number)))

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessOperatorsViolation])


@pytest.mark.parametrize('code', usages)
@pytest.mark.parametrize('number', [
   '5',
   '-0.5',
   '+-0x20',
   '++-0o12',
   '+~0.5',
])
def test_plus_sign_before_numbers_valid(
    assert_errors,
    parse_ast_tree,
    code,
    number,
    default_options,
    mode,
):
    """Testing that there is no useless plus sign before a number."""
    tree = parse_ast_tree(mode(code.format(number)))

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

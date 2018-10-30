# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import (
    UpperCaseAttributeViolation,
)
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor

static_attribute = """
class Test(object):
    {0} = None
"""


@pytest.mark.parametrize('non_snake_case_name', [
    'Abc',
    'A_CONSTANT',
    'AAA',
    'B2',
    'CONST1_bc',
    'camelCase',
    '_A_c',
])
def test_upper_case_class_attributes(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    non_snake_case_name,
    default_options,
):
    """Testing that attribute can not have too short names."""
    tree = parse_ast_tree(static_attribute.format(non_snake_case_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UpperCaseAttributeViolation])
    assert_error_text(visitor, non_snake_case_name)


@pytest.mark.parametrize('snake_case_name', [
    'abc',
    'a_variable',
    'aaa',
    'two_minutes_to_midnight',
    'variable42_5',
    '_a_c',
])
def test_snake_case_class_attributes(
    assert_errors,
    parse_ast_tree,
    snake_case_name,
    default_options,
):
    """Testing that attribute can not have too short names."""
    tree = parse_ast_tree(static_attribute.format(snake_case_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

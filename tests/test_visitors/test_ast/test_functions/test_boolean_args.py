# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BooleanPositionalArgumentViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallVisitor,
)

correct_argument = 'some(0, 1, keyword={0}, other={0})'
wrong_argument = 'some({0}, {0})'


@pytest.mark.parametrize('argument', [
    True,
    False,
    None,
    0,
    1,
    2,
    '[]',
    '""',
    '()',
])
def test_correct_boolean_argument(
    assert_errors,
    parse_ast_tree,
    argument,
    default_options,
):
    """Testing that passing any arguments as keywords is fine."""
    tree = parse_ast_tree(correct_argument.format(argument))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('argument', [
    None,
    0,
    1,
    2,
    '[]',
    '""',
    '()',
])
def test_different_argument(
    assert_errors,
    parse_ast_tree,
    argument,
    default_options,
):
    """Testing that passing non-boolean args is fine."""
    tree = parse_ast_tree(wrong_argument.format(argument))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('argument', [
    True,
    False,
])
def test_wrong_boolean_argument(
    assert_errors,
    parse_ast_tree,
    argument,
    default_options,
):
    """Testing that passing booleans as positional args is restricted."""
    tree = parse_ast_tree(wrong_argument.format(argument))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BooleanPositionalArgumentViolation])

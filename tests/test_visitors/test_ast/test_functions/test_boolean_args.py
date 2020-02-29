# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BooleanPositionalArgumentViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallVisitor,
)

correct_argument = '{1}(0, 1, keyword={0}, other={0})'
correct_three_arguments = '{1}({0}, {0}, {0})'
wrong_argument = '{1}({0}, {0})'

correct_single_argument = '{1}({0})'
wrong_single_argument = '{1}({0}, keyword={0})'

correct_calls = (
    'some',
    'some.get',
    'my.main.pop',
    'some[1].test',
    '[1, 2, 3].pop',
)


@pytest.mark.parametrize('template', [
    correct_argument,
    correct_single_argument,
])
@pytest.mark.parametrize('function', correct_calls)
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
    template,
    function,
    default_options,
):
    """Testing that passing any arguments as keywords is fine."""
    tree = parse_ast_tree(template.format(argument, function))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    correct_three_arguments,
])
@pytest.mark.parametrize('function', [
    'setattr',
    'getattr',
])
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
def test_correct_three_boolean_argument(
    assert_errors,
    parse_ast_tree,
    argument,
    template,
    function,
    default_options,
):
    """Testing that passing any arguments as keywords is fine."""
    tree = parse_ast_tree(template.format(argument, function))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    correct_three_arguments,
])
@pytest.mark.parametrize('function', [
    'nosetattr',
    'other.getattr',
])
@pytest.mark.parametrize('argument', [
    True,
    False,
])
def test_wrong_three_boolean_argument(
    assert_errors,
    parse_ast_tree,
    argument,
    template,
    function,
    default_options,
):
    """Testing that passing any arguments as keywords is fine."""
    tree = parse_ast_tree(template.format(argument, function))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        BooleanPositionalArgumentViolation,
        BooleanPositionalArgumentViolation,
        BooleanPositionalArgumentViolation,
    ])


@pytest.mark.parametrize('template', [
    correct_argument,
    correct_single_argument,
    wrong_argument,
    wrong_single_argument,
])
@pytest.mark.parametrize('function', correct_calls)
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
    template,
    function,
    default_options,
):
    """Testing that passing non-boolean args is fine."""
    tree = parse_ast_tree(template.format(argument, function))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    wrong_argument,
])
@pytest.mark.parametrize('function', [
    'some',
    'get.prop',
    'setattr.custom',
])
@pytest.mark.parametrize('argument', [
    True,
    False,
])
def test_wrong_boolean_argument(
    assert_errors,
    parse_ast_tree,
    argument,
    function,
    template,
    default_options,
):
    """Testing that passing booleans as positional args is restricted."""
    tree = parse_ast_tree(template.format(argument, function))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        BooleanPositionalArgumentViolation,
        BooleanPositionalArgumentViolation,
    ])

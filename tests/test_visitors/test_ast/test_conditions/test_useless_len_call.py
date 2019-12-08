# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    UselessLenCompareViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    IfExpressionVisitor,
    IfStatementVisitor,
)

correct_call1 = 'print(len([]))'
correct_call2 = 'assert len([]) == len([])'
correct_call3 = 'if sum(x): ...'
correct_call4 = 'a if sum(x) else b'

wrong_len_call1 = 'if len(x): ...'
wrong_len_call2 = 'a = 1 if len(x) else 0'
wrong_len_call3 = 'a if len(x) else b'


@pytest.mark.parametrize('code', [
    correct_call1,
    correct_call2,
    correct_call3,
])
def test_useful_len_call(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correct code works."""
    tree = parse_ast_tree(code)

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    correct_call4,
])
def test_useful_if_exp_len_call(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correct code on if exps works."""
    tree = parse_ast_tree(code)

    visitor = IfExpressionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_len_call3,
])
def test_useless_if_exp_len_call(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that incorrect code on if exps raises viol."""
    tree = parse_ast_tree(code)

    visitor = IfExpressionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessLenCompareViolation])


@pytest.mark.parametrize('code', [
    wrong_len_call1,
])
def test_useless_len_call(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that incorrect code raises a violation."""
    tree = parse_ast_tree(code)

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessLenCompareViolation])

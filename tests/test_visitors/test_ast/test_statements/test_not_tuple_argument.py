# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import TUPLE_ARGUMENTS_METHODS
from wemake_python_styleguide.violations.refactoring import (
    NotATupleArgumentViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    WrongMethodArgumentsVisitor,
)


@pytest.mark.parametrize('code', [
    'a = {0}(())',
    'a = {0}((1,))',
    'a = {0}((1, 2, 3))',
    'a = {0}((1,), b)',
    'a = {0}((x for x in some))',
    'a = {0}((x for x in some), b)',
])
@pytest.mark.parametrize('method', [
    *TUPLE_ARGUMENTS_METHODS,
])
def test_passed(
    assert_errors,
    parse_ast_tree,
    code,
    method,
    default_options,
    mode,
):
    """Ensures that tuples arguments are passed."""
    tree = parse_ast_tree(mode(code.format(method)))

    visitor = WrongMethodArgumentsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'a = {0}([])',
    'a = {0}({1}1{2})',
    'a = {0}({1}1, 2, 3{2})',
    'a = {0}({1}1{2}, b)',
    'a = {0}({1}1{2}, b, c)',
    'a = {0}({1}1{2}, b, {1}2{2})',
    'a = {0}({1}x for x in some{2})',
])
@pytest.mark.parametrize('method', [
    *TUPLE_ARGUMENTS_METHODS,
])
@pytest.mark.parametrize('braces', ['[]', '{}'])  # noqa: P103
def test_no_passed(
    assert_errors,
    parse_ast_tree,
    code,
    method,
    braces,
    default_options,
):
    """Ensures that non-tuples arguments are violated."""
    tree = parse_ast_tree(code.format(method, braces[0], braces[1]))

    visitor = WrongMethodArgumentsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NotATupleArgumentViolation])


@pytest.mark.parametrize('code', [
    'a = {0}_func([1])',
])
@pytest.mark.parametrize('method', [
    *TUPLE_ARGUMENTS_METHODS,
])
def test_no_checkable(
    assert_errors,
    parse_ast_tree,
    code,
    method,
    default_options,
    mode,
):
    """Ensures that non checkable situations are skipped."""
    tree = parse_ast_tree(mode(code.format(method)))

    visitor = WrongMethodArgumentsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

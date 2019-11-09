# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import TUPLE_ARGUMENTS_METHODS
from wemake_python_styleguide.violations.refactoring import (
    ForceTupleArgumentsViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    WrongMethodParametersVisitor,
)


@pytest.mark.parametrize('code', [
    'a = {0}((1,))',
    'a = {0}((1,), b)',
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

    visitor = WrongMethodParametersVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'a = {0}([1])',
    'a = {0}([1], 1)',
    'a = {0}([1], b)',
    'a = {0}([1], b, c)',
    'a = {0}([1], b, [2])',
    'a = {0}({{1}})',
])
@pytest.mark.parametrize('method', [
    *TUPLE_ARGUMENTS_METHODS,
])
def test_no_passed(
    assert_errors,
    parse_ast_tree,
    code,
    method,
    default_options,
    mode,
):
    """Ensures that non-tuples arguments are violated."""
    tree = parse_ast_tree(mode(code.format(method)))

    visitor = WrongMethodParametersVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ForceTupleArgumentsViolation])


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

    visitor = WrongMethodParametersVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

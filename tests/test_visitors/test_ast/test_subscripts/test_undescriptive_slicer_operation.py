# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    UndescriptiveSliceOperationViolation,
)
from wemake_python_styleguide.visitors.ast.subscripts import SubscriptVisitor

usage_template = 'constant[{0}]'


@pytest.mark.parametrize('expression', [
    '::-1',
    ':',
    '::',
])
def test_undescriptive_slice_operation(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that undescriptive slice operations are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SubscriptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UndescriptiveSliceOperationViolation])


@pytest.mark.parametrize('expression', [
    '3:',
    '3::2',
    ':7',
    ':7:2',
    '3:7',
    '3:7:2',
    '::3',
])
def test_good_slice_operation(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that other slice operations are allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SubscriptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

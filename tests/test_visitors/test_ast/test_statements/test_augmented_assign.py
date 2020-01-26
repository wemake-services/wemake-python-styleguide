# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    AugmentedAssignPatternViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    AssignmentPatternsVisitor,
)

OPERATIONS = frozenset((
    '+',
    '-',
    '*',
    '/',
    '%',
    '**',
    '&',
    '|',
    '^',
    '>>',
    '<<',
))


@pytest.mark.parametrize('code', [
    'a {0}= b',
])
@pytest.mark.parametrize('operation', OPERATIONS)
def test_augmented_assign(
    assert_errors,
    parse_ast_tree,
    code,
    operation,
    default_options,
    mode,
):
    """Ensures that augemented assignment are not violated."""
    tree = parse_ast_tree(mode(code.format(operation)))

    visitor = AssignmentPatternsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'a = a {0} b',
])
@pytest.mark.parametrize('operation', OPERATIONS)
def test_no_augmented_assign(
    assert_errors,
    parse_ast_tree,
    code,
    operation,
    default_options,
    mode,
):
    """Ensures force augmented assignments."""
    tree = parse_ast_tree(mode(code.format(operation)))

    visitor = AssignmentPatternsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [AugmentedAssignPatternViolation])


@pytest.mark.parametrize('code', [
    'a = a {0} b + c',
    'a = b {0} a + c',
    'a = (a {0} b) - c',
    'a = b {0} c',
    'a = b {0} a',
])
@pytest.mark.parametrize('operation', OPERATIONS)
def test_no_checkable_assign(
    assert_errors,
    parse_ast_tree,
    code,
    operation,
    default_options,
    mode,
):
    """Ensures that complex expressions are not checked."""
    tree = parse_ast_tree(mode(code.format(operation)))

    visitor = AssignmentPatternsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

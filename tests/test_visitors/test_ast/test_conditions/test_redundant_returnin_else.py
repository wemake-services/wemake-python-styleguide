# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    RedundantReturningElseViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor

function_level_condition = """
def function():
    if some_condition:
        {0}
    else:
        ...
"""

for_loop_level_condition = """
def wrapper():
    for _ in some_iterable:
        if some_condition:
            {0}
        else:
            ...
"""

while_loop_level_condition = """
while True:
    if some_condition:
        {0}
    else:
        ...
"""

module_level_condition = """
if some_condition:
    {0}
else:
    ...
"""


@pytest.mark.parametrize('code', [
    'return',
    'return True',
    'raise ValueError()',
])
def test_else_that_can_be_removed_in_function(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(mode(function_level_condition.format(code)))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantReturningElseViolation])


@pytest.mark.parametrize('template', [
    for_loop_level_condition,
    while_loop_level_condition,
])
@pytest.mark.parametrize('code', [
    'break',
    'raise ValueError()',
])
def test_else_that_can_be_removed_in_loop(
    assert_errors,
    parse_ast_tree,
    template,
    code,
    default_options,
    mode,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantReturningElseViolation])


@pytest.mark.parametrize('code', [
    'raise ValueError()',
])
def test_else_that_can_be_removed_in_module(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(module_level_condition.format(code))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantReturningElseViolation])


@pytest.mark.parametrize('template', [
    function_level_condition,
    for_loop_level_condition,
    while_loop_level_condition,
    module_level_condition,
])
@pytest.mark.parametrize('code', [
    'print()',
    'new_var = 1',
])
def test_else_that_can_not_be_removed(
    assert_errors,
    parse_ast_tree,
    template,
    code,
    default_options,
    mode,
):
    """Testing that extra ``else`` blocks can not be removed."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BlockAndLocalOverlapViolation,
)
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor

# Loops:

for_loop1 = 'for {0} in some():'
for_loop2 = 'for {0}, second in some():'
for_loop3 = 'for first, *{0} in some():'

# Wrong usages:

for_template1 = """
def function():
    {0}
        ...
    {1}
"""

for_template2 = """
def function():
    {0}
        {1}
"""

for_template3 = """
class Test(object):
    def method(self):
        {0}
            ...
        {1}
"""

for_template4 = """
class Test(object):
    def method(self):
        {0}
            {1}
"""


@pytest.mark.parametrize('for_statement', [
    for_loop1,
    for_loop2,
    for_loop3,
])
@pytest.mark.parametrize('context', [
    for_template1,
    for_template2,
    for_template3,
    for_template4,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_for_block_overlap(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    for_statement,
    assign_statement,
    context,
    variable_name,
    default_options,
    mode,
):
    """Ensures that overlaping variables exist."""
    code = context.format(
        for_statement.format(variable_name),
        assign_statement.format(variable_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BlockAndLocalOverlapViolation])
    assert_error_text(visitor, variable_name)


@pytest.mark.parametrize('for_statement', [
    for_loop1,
    for_loop2,
    for_loop3,
])
@pytest.mark.parametrize('context', [
    for_template1,
    for_template2,
    for_template3,
    for_template4,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_for_block_usage(
    assert_errors,
    parse_ast_tree,
    for_statement,
    context,
    variable_name,
    default_options,
    mode,
):
    """Ensures using variables is fine."""
    code = context.format(
        for_statement.format(variable_name),
        'print({0})'.format(variable_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('for_statement', [
    for_loop1,
    for_loop2,
    for_loop3,
])
@pytest.mark.parametrize('context', [
    for_template1,
    for_template2,
    for_template3,
    for_template4,
])
@pytest.mark.parametrize('first_name, second_name', [
    ('unique_name', 'other_name'),
])
def test_for_block_correct(
    assert_errors,
    parse_ast_tree,
    for_statement,
    assign_statement,
    context,
    first_name,
    second_name,
    default_options,
    mode,
):
    """Ensures that different variables do not overlap."""
    code = context.format(
        for_statement.format(first_name),
        assign_statement.format(second_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

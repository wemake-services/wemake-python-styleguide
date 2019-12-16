# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BlockAndLocalOverlapViolation,
)
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor

# Context managers:

with1 = 'with open() as {0}:'
with2 = 'with open() as ({0}, second):'
with3 = 'with open() as (first, *{0}):'
with4 = 'with open() as {0}, close() as second:'
with5 = 'with open() as first, close() as {0}:'

# Wrong usages:

with_template1 = """
def function():
    {0}
        ...
    {1}
"""

with_template2 = """
def function():
    {0}
        {1}
"""

with_template3 = """
class Test(object):
    def method(self):
        {0}
            ...
        {1}
"""

with_template4 = """
class Test(object):
    def method(self):
        {0}
            {1}
"""


@pytest.mark.parametrize('with_statement', [
    with1,
    with2,
    with3,
    with4,
    with5,
])
@pytest.mark.parametrize('context', [
    with_template1,
    with_template2,
    with_template3,
    with_template4,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_with_block_overlap(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    with_statement,
    assign_and_annotation_statement,
    context,
    variable_name,
    default_options,
    mode,
):
    """Ensures that overlaping variables exist."""
    code = context.format(
        with_statement.format(variable_name),
        assign_and_annotation_statement.format(variable_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BlockAndLocalOverlapViolation])
    assert_error_text(visitor, variable_name)


@pytest.mark.parametrize('with_statement', [
    with1,
    with2,
    with3,
    with4,
    with5,
])
@pytest.mark.parametrize('context', [
    with_template1,
    with_template2,
    with_template3,
    with_template4,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_with_block_usage(
    assert_errors,
    parse_ast_tree,
    with_statement,
    context,
    variable_name,
    default_options,
    mode,
):
    """Ensures using variables is fine."""
    code = context.format(
        with_statement.format(variable_name),
        'print({0})'.format(variable_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('with_statement', [
    with1,
    with2,
    with3,
    with4,
    with5,
])
@pytest.mark.parametrize('context', [
    with_template1,
    with_template2,
    with_template3,
    with_template4,
])
@pytest.mark.parametrize(('first_name', 'second_name'), [
    ('unique_name', 'unique'),
    ('_', '_'),
])
def test_with_block_correct(
    assert_errors,
    parse_ast_tree,
    with_statement,
    assign_and_annotation_statement,
    context,
    first_name,
    second_name,
    default_options,
    mode,
):
    """Ensures that different variables do not overlap."""
    code = context.format(
        with_statement.format(first_name),
        assign_and_annotation_statement.format(second_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

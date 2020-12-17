import pytest

from wemake_python_styleguide.violations.best_practices import (
    BlockAndLocalOverlapViolation,
)
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor

# Contexts:
context = """
{0}

{1}
"""

# Block statements:
block_statement1 = 'from some import {0}, {1}'


@pytest.mark.parametrize('block_statement', [
    block_statement1,
])
@pytest.mark.parametrize('local_statement', [
    '{0} = func({0})',
    '{0} = {0}(arg)',
    '{0} = {0} + 1',
    '{0} = {0}.attr',
    '{0} = {0}["key"]',
    '{0} = d[{0}]',
    '{0} = d[{0}:1]',
    '{0}: type = func({0})',
    '{0}: type = {0}(arg)',
    '{0}: type = {0} + 1',
    '{0}: type = {0}.attr',
    '{0}: type = {0}["key"]',
    '{0}: type = d[{0}]',
    '{0}, {1} = {0}({1})',
    '{0}, {1} = {0} * {1}',
    '{1}, {0} = ({1}, {0})',
    '{1}, *{0} = ({1}, {0})',
])
@pytest.mark.parametrize(('first_name', 'second_name'), [
    ('no_raise', 'used'),
])
def test_reuse_no_overlap(
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
    block_statement,
    local_statement,
    first_name,
    second_name,
):
    """Ensures that overlapping variables does not exist."""
    code = context.format(
        block_statement.format(first_name, second_name),
        local_statement.format(first_name, second_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('block_statement', [
    block_statement1,
])
@pytest.mark.parametrize('local_statement', [
    '{0} = func({1})',
    '{0} = {1}(arg)',
    '{0} = {1} + 1',
    '{0} = {1}.attr',
    '{0} = {1}["key"]',
    '{0} = d[{1}]',
    '{0} = d[{1}:1]',
    '{0}: {1}',
    '{0}: type = func({1})',
    '{0}: type = {1}(arg)',
    '{0}: type = {1} + 1',
    '{0}: type = {1}.attr',
    '{0}: type = {1}["key"]',
    '{0}: type = d[{1}]',
    '{0}, {1} = {0}({0})',
    '{0}, {1} = {1} * {1}',
    '{1}, {0} = ({0}, {0})',
    '{1}, *{0} = ({1}, {1})',
])
@pytest.mark.parametrize(('first_name', 'second_name'), [
    ('no_raise', 'used'),
])
def test_reuse_overlap(
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
    block_statement,
    local_statement,
    first_name,
    second_name,
):
    """Ensures that overlapping variables exist no."""
    code = context.format(
        block_statement.format(first_name, second_name),
        local_statement.format(first_name, second_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BlockAndLocalOverlapViolation])

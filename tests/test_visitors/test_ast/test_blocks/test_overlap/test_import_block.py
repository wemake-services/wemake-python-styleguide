# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BlockAndLocalOverlapViolation,
)
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor

# Imports:

import_block = 'import {0}'
import_block_as = 'import some as {0}'
from_import_block = 'from some import {0}'
from_import_block_as = 'from some import some as {0}'

import_template1 = """
{0}
{1}
"""

import_template2 = """
def context():
    {0}
    {1}
"""

import_template3 = """
class Test(object):
    def context(self):
        {0}
        {1}
"""


@pytest.mark.parametrize('import_statement', [
    import_block,
    import_block_as,
    from_import_block,
    from_import_block_as,
])
@pytest.mark.parametrize('context', [
    import_template1,
    import_template2,
    import_template3,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_import_block_overlap(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    import_statement,
    assign_statement,
    context,
    variable_name,
    default_options,
    mode,
):
    """Ensures that overlaping variables exist."""
    code = context.format(
        import_statement.format(variable_name),
        assign_statement.format(variable_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BlockAndLocalOverlapViolation])
    assert_error_text(visitor, variable_name)


@pytest.mark.parametrize('import_statement', [
    import_block,
    import_block_as,
    from_import_block,
    from_import_block_as,
])
@pytest.mark.parametrize('context', [
    import_template1,
    import_template2,
    import_template3,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise_if_assigned',
])
def test_import_block_usage(
    assert_errors,
    parse_ast_tree,
    import_statement,
    context,
    variable_name,
    default_options,
    mode,
):
    """Ensures using variables is fine."""
    code = context.format(
        import_statement.format(variable_name),
        'print({0})'.format(variable_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('import_statement', [
    import_block,
    import_block_as,
    from_import_block,
    from_import_block_as,
])
@pytest.mark.parametrize('context', [
    import_template1,
    import_template2,
    import_template3,
])
@pytest.mark.parametrize(('first_name', 'second_name'), [
    ('unique_name', '_unique_name'),
    ('_', '_'),
])
def test_import_block_correct(
    assert_errors,
    parse_ast_tree,
    import_statement,
    assign_statement,
    context,
    first_name,
    second_name,
    default_options,
    mode,
):
    """Ensures that different variables do not overlap."""
    code = context.format(
        import_statement.format(first_name),
        assign_statement.format(second_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

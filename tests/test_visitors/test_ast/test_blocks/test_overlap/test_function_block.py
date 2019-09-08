# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BlockAndLocalOverlapViolation,
)
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor

# Functions:

function_def1 = 'def {0}():'

# Wrong usages:

function_template1 = """
{0}
    ...

{1}
"""

function_template2 = """
{1}

{0}
    ...
"""

# Correct usages:

method_template1 = """
{1}

class Test(object):
    {0}
        ...
"""

method_template2 = """
class Test(object):
    {0}
        ...

{1}
"""


@pytest.mark.parametrize('function_statement', [
    function_def1,
])
@pytest.mark.parametrize('context', [
    function_template1,
    function_template2,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_function_block_overlap(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    function_statement,
    assign_statement,
    context,
    variable_name,
    default_options,
    mode,
):
    """Ensures that overlaping variables exist."""
    code = context.format(
        function_statement.format(variable_name),
        assign_statement.format(variable_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BlockAndLocalOverlapViolation])
    assert_error_text(visitor, variable_name)


@pytest.mark.parametrize('function_statement', [
    function_def1,
])
@pytest.mark.parametrize('context', [
    method_template1,
    method_template2,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_method_block_overlap(
    assert_errors,
    parse_ast_tree,
    function_statement,
    assign_statement,
    context,
    variable_name,
    default_options,
    mode,
):
    """Ensures that overlaping variables exist."""
    code = context.format(
        function_statement.format(variable_name),
        assign_statement.format(variable_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('function_statement', [
    function_def1,
])
@pytest.mark.parametrize('context', [
    function_template1,
    function_template2,
    method_template1,
    method_template2,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_function_block_usage(
    assert_errors,
    parse_ast_tree,
    function_statement,
    context,
    variable_name,
    default_options,
    mode,
):
    """Ensures using variables is fine."""
    code = context.format(
        function_statement.format(variable_name),
        'print({0})'.format(variable_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('function_statement', [
    function_def1,
])
@pytest.mark.parametrize('context', [
    function_template1,
    function_template2,
    method_template1,
    method_template2,
])
@pytest.mark.parametrize(('first_name', 'second_name'), [
    ('unique_name', 'unique_name1'),
    ('_', '_'),
])
def test_function_block_correct(
    assert_errors,
    parse_ast_tree,
    function_statement,
    assign_statement,
    context,
    first_name,
    second_name,
    default_options,
    mode,
):
    """Ensures that different variables do not overlap."""
    code = context.format(
        function_statement.format(first_name),
        assign_statement.format(second_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


pipeline = """
def pipeline(function):
    return
"""

overload_template = """
{0}
{1}
{1}
"""


@pytest.mark.parametrize('import_overload', [
    """
@overload
    """,
    """
@typing.overload
    """,
])
def test_function_overload(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    import_overload,
    mode,
):
    """
    Ensures that overload from typing do not overlap.
    """
    code = overload_template.format(import_overload, pipeline)
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('decorator_tempate', [
    """
@typing.func
    """,
    """
@module.overload
    """,
    """
@decorate
    """,
])
def test_no_function_overload(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    decorator_tempate,
    mode,
):
    """
    Ensures that not overload from typing do overlap.
    """
    code = overload_template.format(decorator_tempate, pipeline)
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BlockAndLocalOverlapViolation, ])

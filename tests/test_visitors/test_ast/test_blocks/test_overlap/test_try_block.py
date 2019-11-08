# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BlockAndLocalOverlapViolation,
)
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor

# Exception handling:

except_block1 = 'except Exception as {0}:'
except_block2 = 'except (TypeError, ValueError) as {0}:'

# Wrong usages:

try_template1 = """
try:
    {1}
{0}
    ...
"""

try_template2 = """
try:
    ...
{0}
    {1}
"""

try_template3 = """
try:
    ...
{0}
    ...
{1}
"""

try_template4 = """
def function():
    try:
        {1}
    {0}
        ...
"""

try_template5 = """
def function():
    try:
        ...
    {0}
        {1}
"""

try_template6 = """
def function():
    try:
        ...
    {0}
        ...
    {1}
"""

try_template7 = """
class Test(object):
    def method(self):
        try:
            {1}
        {0}
            ...
"""

try_template8 = """
class Test(object):
    def method(self):
        try:
            ...
        {0}
            {1}
"""

try_template9 = """
class Test(object):
    def method(self):
        try:
            ...
        {0}
            ...
        {1}
"""


@pytest.mark.parametrize('except_statement', [
    except_block1,
    except_block2,
])
@pytest.mark.parametrize('context', [
    try_template1,
    try_template2,
    try_template3,
    try_template4,
    try_template5,
    try_template6,
    try_template7,
    try_template8,
    try_template9,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_except_block_overlap(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    except_statement,
    assign_statement,
    context,
    variable_name,
    default_options,
    mode,
):
    """Ensures that overlaping variables exist."""
    code = context.format(
        except_statement.format(variable_name),
        assign_statement.format(variable_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BlockAndLocalOverlapViolation])
    assert_error_text(visitor, variable_name)


@pytest.mark.parametrize('except_statement', [
    except_block1,
    except_block2,
])
@pytest.mark.parametrize('context', [
    try_template1,
    try_template2,
    try_template3,
    try_template4,
    try_template5,
    try_template6,
    try_template7,
    try_template8,
    try_template9,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_except_block_usage(
    assert_errors,
    parse_ast_tree,
    except_statement,
    context,
    variable_name,
    default_options,
    mode,
):
    """Ensures using variables is fine."""
    code = context.format(
        except_statement.format(variable_name),
        'print({0})'.format(variable_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('except_statement', [
    except_block1,
    except_block2,
])
@pytest.mark.parametrize('context', [
    try_template1,
    try_template2,
    try_template3,
    try_template4,
    try_template5,
    try_template6,
    try_template7,
    try_template8,
    try_template9,
])
@pytest.mark.parametrize(('first_name', 'second_name'), [
    ('unique_name', 'unique_name2'),
    ('_', '_'),
])
def test_except_block_correct(
    assert_errors,
    parse_ast_tree,
    except_statement,
    assign_and_annotation_statement,
    context,
    first_name,
    second_name,
    default_options,
    mode,
):
    """Ensures that different variables do not overlap."""
    code = context.format(
        except_statement.format(first_name),
        assign_and_annotation_statement.format(second_name),
    )
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

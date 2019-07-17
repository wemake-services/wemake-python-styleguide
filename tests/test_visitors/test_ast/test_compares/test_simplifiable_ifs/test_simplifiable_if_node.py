# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    SimplifiableIfViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongConditionalVisitor,
)

# Correct:

simple_if_template = """
if some_value:
    {0} = {1}
else:
    {2} = {3}
"""

simple_if_typed_template = """
if some_value:
    {0}: int = {1}
else:
    {2}: str = {3}
"""

# Wrong:

complex_if_template = """
if some_value:
    {0} = {1}
    print(some_value)
else:
    {2} = {3}
    print(some_value)
"""

nested_if_template = """
if some_value:
    {0} = {1}
    if other:
        {2} = {3}
"""

near_if_template = """
if some_value:
    {0} = {1}
if other:
    {2} = {3}
"""

near_elif_template = """
if some_value:
    {0} = {1}
elif other:
    {2} = {3}
"""

near_elif_typed_template = """
if some_value:
    {0}: int = {1}
elif other:
    {2}: str = {3}
"""

single_if_template = """
if some_value:
    {0} = {1}
    {2} = {3}
"""


@pytest.mark.parametrize('code', [
    complex_if_template,
    nested_if_template,
    near_if_template,
    near_elif_template,
    near_elif_typed_template,
    single_if_template,
])
@pytest.mark.parametrize('comparators', [
    ('variable', 'True', 'variable', 'False'),
    ('variable', 'False', 'variable', 'True'),
    ('variable', 'None', 'variable', 'True'),
    ('some_name', 'True', 'variable', 'False'),
    ('variable', 'False', 'some_name', 'True'),
])
def test_not_simplifiable_node(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that regular nodes work well."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    simple_if_template,
    simple_if_typed_template,
])
@pytest.mark.parametrize('comparators', [
    ('variable', 'True', 'variable', 'False'),
    ('variable', 'False', 'variable', 'True'),
    ('variable[0]', 'True', 'variable[0]', 'False'),
    ('variable.attr', 'False', 'variable.attr', 'True'),
])
def test_simplifiable_node(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that simplifiable nodes work well."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [SimplifiableIfViolation])


@pytest.mark.parametrize('code', [
    simple_if_template,
    simple_if_typed_template,
    complex_if_template,
])
@pytest.mark.parametrize('comparators', [
    ('variable', 'None', 'variable', 'False'),
    ('variable', 'None', 'variable', 'True'),
    ('variable1[0]', 'True', 'variable2[0]', 'False'),
    ('variable[0]', 'True', 'variable[1]', 'False'),
    ('variable.attr1', 'False', 'variable.attr2', 'True'),
])
def test_not_simplifiable_node_bad_values(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that simplifiable nodes work well with incorrect patterns."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    simple_if_template,
    complex_if_template,
])
@pytest.mark.parametrize('comparators', [
    ('variable1 = variable2', 'True', 'variable1 = variable2', 'False'),
    ('variable2 = variable1', 'True', 'variable1 = variable2', 'False'),
    ('variable1 = variable2', 'True', 'variable2 = variable1', 'False'),
    ('variable1 = variable2', 'False', 'variable1 = variable2', 'True'),
])
def test_not_simplifiable_node_multiple(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that simplifiable nodes work well with incorrect patterns."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

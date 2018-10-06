# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
)
from wemake_python_styleguide.visitors.ast.order import WrongOrderVisitor

# templates to be checked

if_with_is = """
if {0} is {1}:
    return 1
"""

if_with_is_not = """
if {0} is not {1}:
    return 1
"""

if_with_eq = """
if {0} == {1}:
    return 1
"""

if_with_not_eq = """
if {0} != {1}:
    return 1
"""

if_with_gt = """
if {0} > {1}:
    return 1
"""

if_with_lt = """
if {0} < {1}:
    return 1
"""

ternary = """
ternary = 5 if {0} > {1} else 6
"""

while_construct = """
while {0} > {1}:
    return 1
"""

if_with_compound_expr = """
if {0} > {1} and {0} < {1}:
    return 1
"""

if_with_chained_comparisons = """
if {0} < {1} < {2}:
    return 1
"""


@pytest.mark.parametrize('code', [
    if_with_is,
    if_with_is_not,
    if_with_eq,
    if_with_not_eq,
    if_with_lt,
    if_with_gt,
    ternary,
    while_construct,
    if_with_compound_expr,
])

@pytest.mark.parametrize('variable1,variable2', [
    ('a', 'b'),
])

def test_comparison_variables(
    assert_errors,
    parse_ast_tree,
    code,
    variable1,
    variable2,
    default_options,
):
    """Testing that comparisons work well for the case of all variables"""
    tree = parse_ast_tree(code.format(variable1, variable2))

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [
    if_with_is,
    if_with_is_not,
    if_with_eq,
    if_with_not_eq,
    if_with_lt,
    if_with_gt,
    ternary,
    while_construct,
    if_with_compound_expr,
])

@pytest.mark.parametrize('variable,literal', [
    ('a', 1),
    ('a', 2.3),
    ('a', [1,2]),
])

def test_comparison_literal_right(
    assert_errors,
    parse_ast_tree,
    code,
    variable,
    literal,
    default_options,
):
    """Testing that comparisons work well with literal on right and argument on left"""
    tree = parse_ast_tree(code.format(variable, literal))

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [
    if_with_is,
    if_with_is_not,
    if_with_eq,
    if_with_not_eq,
    if_with_lt,
    if_with_gt,
    ternary,
    while_construct,
    if_with_compound_expr,
])

@pytest.mark.parametrize('literal,variable', [
    (1, 'a'),
    (2.3, 'a'),
    ([1,2], 'a'),
])

def test_wrong_comparison(
    assert_errors,
    parse_ast_tree,
    code,
    literal,
    variable,
    default_options,
):
    """Testing that violations are raised when inconsistent comparisons are used."""
    tree = parse_ast_tree(code.format(literal, variable))
    
    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()
    
    assert_errors(visitor, [ComparisonOrderViolation])

@pytest.mark.parametrize('code', [
    if_with_chained_comparisons,
])

@pytest.mark.parametrize('literal1,variable,literal2', [
    (0, 'a', 1),
])

def test_consistent_chained_comparison(
    assert_errors,
    parse_ast_tree,
    code,
    literal1,
    variable,
    literal2,
    default_options,
):
    """Testing that comparisons work well for consistent chained comparison"""
    tree = parse_ast_tree(code.format(literal1, variable, literal2))
    
    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()
    
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [
    if_with_chained_comparisons,
])

@pytest.mark.parametrize('literal1,literal2,variable', [
    (0, 5, 'x'),
])

def test_consistent_chained_comparison(
    assert_errors,
    parse_ast_tree,
    code,
    literal1,
    literal2,
    variable,
    default_options,
):
    """Testing that violations are raised when inconsistent chained comparisons are used."""
    tree = parse_ast_tree(code.format(literal1, literal2, variable))
    
    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()
    
    assert_errors(visitor, [ComparisonOrderViolation])
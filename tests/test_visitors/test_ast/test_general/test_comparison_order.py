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
@pytest.mark.parametrize('variable', [
    ('a', 'b'),
])
def test_comparison_variables(
    assert_errors,
    parse_ast_tree,
    code,
    variable,
    default_options,
):
    """Testing that comparisons work well for the case of all variables"""
    tree = parse_ast_tree(code.format(variable[0], variable[1]))

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
@pytest.mark.parametrize('var_lit', [
    ('a', 1),
    ('a', 2.3),
    ('a', [1, 2]),
])
def test_comparison_literal_right(
    assert_errors,
    parse_ast_tree,
    code,
    var_lit,
    default_options,
):
    """Testing that comparisons work well with argument on left"""
    tree = parse_ast_tree(code.format(var_lit[0], var_lit[1]))

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
])
@pytest.mark.parametrize('lit_var', [
    (1, 'a'),
    (2.3, 'a'),
    ([1, 2], 'a'),
])
def test_wrong_comparison(
    assert_errors,
    parse_ast_tree,
    code,
    lit_var,
    default_options,
):
    """Testing that violations are raised when inconsistent comparisons are used."""
    tree = parse_ast_tree(code.format(lit_var[0], lit_var[1]))

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()
    
    assert_errors(visitor, [ComparisonOrderViolation])


@pytest.mark.parametrize('code', [
    if_with_compound_expr,
])
@pytest.mark.parametrize('lit_var', [
    ([1, 2], 'a'), 
])
def test_wrong_compound_comparison(
    assert_errors,
    parse_ast_tree,
    code,
    lit_var,
    default_options,
):
    """Testing that violations are raised when inconsistent comparisons are used."""
    tree = parse_ast_tree(code.format(lit_var[0], lit_var[1]))

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComparisonOrderViolation, ComparisonOrderViolation])


@pytest.mark.parametrize('code', [
    if_with_chained_comparisons,
])
@pytest.mark.parametrize('lit_var_lit', [
    (0, 'a', 1),
])
def test_consistent_chained_comparison(
    assert_errors,
    parse_ast_tree,
    code,
    lit_var_lit,
    default_options
):
    """Testing that comparisons work well for consistent chained comparison"""
    tree = parse_ast_tree(code.format(lit_var_lit[0], lit_var_lit[1], lit_var_lit[2]))
    
    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    if_with_chained_comparisons,
])
@pytest.mark.parametrize('lit_lit_var', [
    (0, 5, 'x'),
])
def test_consistent_chained_comparison(
    assert_errors,
    parse_ast_tree,
    code,
    lit_lit_var,
    default_options
):
    """Testing that violations are raised when inconsistent chained comparisons are used."""
    tree = parse_ast_tree(code.format(lit_lit_var[0], lit_lit_var[1], lit_lit_var[2]))

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComparisonOrderViolation])

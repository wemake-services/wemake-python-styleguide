# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    MultilineConditionsViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor

incorrect_conditions1 = """if some and (
    other == 1
):
    ...
"""

incorrect_conditions2 = """
if some or (
    other == 1
):
        ...
"""

incorrect_conditions3 = """if some and some_function(
    other,
):
    ...
"""

incorrect_conditions4 = """
if some or some_func(
    other,
):
        ...
"""

incorrect_conditions5 = """
if very_long_call_name(
    long_parameter_name=long_variable_name,
):
    ...
"""

correct_conditions1 = """
if some and other or something:
    ...
"""

correct_conditions2 = """
if some_func(k) and (some or other):
    ...
"""

correct_conditions3 = """
if (some_func(k) and some) or other in (1,2,3):
    ...
"""

correct_conditions4 = """
if one:
    if two:
         ...
"""

@pytest.mark.parametrize('code', [
    incorrect_conditions1,
    incorrect_conditions2,
    incorrect_conditions3,
    incorrect_conditions4,
    incorrect_conditions5,
])
def test_incorrect_multiline_conditions(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing multiline conditions."""
    tree = parse_ast_tree(mode(code))
    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [MultilineConditionsViolation])


@pytest.mark.parametrize('code', [
    correct_conditions1,
    correct_conditions2,
    correct_conditions3,
    correct_conditions4,
])
def test_correct_multiline_conditions(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing multiline conditions."""
    tree = parse_ast_tree(mode(code))
    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

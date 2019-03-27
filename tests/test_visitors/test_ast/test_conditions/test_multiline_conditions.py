# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    MultilineConditionsViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor

incorrect_and_conditions1 = """if some and (
    other == 1
):
    ...
"""

incorrect_or_conditions1 = """
if some or (
    other==1
):
        ...
"""

incorrect_and_conditions2 = """if some and some_function(
    other,
):
    ...
"""

incorrect_or_conditions2 = """
if some or some_func(
    other,
):
        ...
"""


@pytest.mark.parametrize('code', [
    incorrect_and_conditions1,
    incorrect_and_conditions2,
    incorrect_or_conditions1,
    incorrect_or_conditions2,
])
def test_multiline_conditions(
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

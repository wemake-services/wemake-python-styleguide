# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor

incorrect_and_conditions1 = """
if some_condition and some_condition:
        ...
"""

incorrect_or_conditions1 = """
if some_condition or some_condition:
        ...
"""


@pytest.mark.parametrize('code', [
    incorrect_and_conditions1,
    incorrect_or_conditions1,
])
def test_multiline_conditions(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that extra ``else`` blocks can not be removed."""
    tree = parse_ast_tree(mode(code))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

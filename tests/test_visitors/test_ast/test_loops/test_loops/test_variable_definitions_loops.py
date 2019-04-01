# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    LoopVariableDefinitionViolation,
)
from wemake_python_styleguide.visitors.ast.loops import (
    WrongLoopDefinitionVisitor,
)

for_loop_def = """
def wrapper():
    for {0} in some:
        ...
"""


@pytest.mark.parametrize('definition', [
    'xy[0]',
    'xy.attr',
    'xy["key"]',
    '(valid, invalid.attr)',
    '(invalid.attr, valid)',
])
def test_wrong_definition_loop(
    assert_errors,
    parse_ast_tree,
    definition,
    default_options,
    mode,
):
    """Ensures that wrong definitions are not allowed."""
    tree = parse_ast_tree(mode(for_loop_def.format(definition)))

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [LoopVariableDefinitionViolation])


@pytest.mark.parametrize('definition', [
    'xy',
    '(valid1, valid2)',
])
def test_correct_definition_loop(
    assert_errors,
    parse_ast_tree,
    definition,
    default_options,
    mode,
):
    """Ensures that correct definitions are allowed."""
    tree = parse_ast_tree(mode(for_loop_def.format(definition)))

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

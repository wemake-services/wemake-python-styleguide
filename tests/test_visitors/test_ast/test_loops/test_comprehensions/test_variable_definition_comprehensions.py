# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    LoopVariableDefinitionViolation,
)
from wemake_python_styleguide.visitors.ast.loops import (
    WrongLoopDefinitionVisitor,
)

list_comprehension = """
def container():
    nodes = [0 for {0} in some]
"""

generator_expression = """
def container():
    nodes = (0 for {0} in some)
"""

set_comprehension = """
def container():
    nodes = {{0 for {0} in some}}
"""


@pytest.mark.parametrize('code', [
    list_comprehension,
    generator_expression,
    set_comprehension,
])
@pytest.mark.parametrize('definition', [
    'xy.attr',
    'xy["key"]',
    '(xy[0], y)',
    '(y, xy.attr)',
])
def test_wrong_definitions_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    definition,
    default_options,
    mode,
):
    """Testing that using wrong variables is not allowed."""
    tree = parse_ast_tree(mode(code.format(definition)))

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [LoopVariableDefinitionViolation])


@pytest.mark.parametrize('code', [
    list_comprehension,
    generator_expression,
    set_comprehension,
])
@pytest.mark.parametrize('definition', [
    'xy',
    '(y, xy)',
])
def test_comprehension_without_bad_definitions(
    assert_errors,
    parse_ast_tree,
    code,
    definition,
    default_options,
    mode,
):
    """Testing that regular comprehensions are allowed."""
    tree = parse_ast_tree(mode(code.format(definition)))
    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

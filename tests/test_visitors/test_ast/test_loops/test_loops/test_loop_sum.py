# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    ImplicitSumViolation,
)
from wemake_python_styleguide.visitors.ast.loops import (
    WrongLoopDefinitionVisitor,
)

for_loop_template = """
def function():
    value = 0
    for index in some:
        {0}
"""


@pytest.mark.parametrize('template', [
    for_loop_template,
])
@pytest.mark.parametrize('code', [
    'value += index',
    'value += 1',
    'value += index.prop',
    'value += index[key]',
    'value += index.method()',

    'other += 1',
    'index += value',
    'value += "str"',
])
def test_implicit_sum(
    assert_errors,
    parse_ast_tree,
    code,
    template,
    default_options,
    mode,
):
    """Ensures that implicit ``sum()`` calls are not allowed."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImplicitSumViolation])


@pytest.mark.parametrize('template', [
    for_loop_template,
])
@pytest.mark.parametrize('code', [
    'sum(some)',
    'value -= 1',
    'print(index)',
    'index += value\n        print(index)',  # two nodes in a body
    'obj.attr += 1',
    'obj[key] += index',
])
def test_regular_loops(
    assert_errors,
    parse_ast_tree,
    code,
    template,
    default_options,
    mode,
):
    """Ensures that correct ``sum()`` calls are allowed."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

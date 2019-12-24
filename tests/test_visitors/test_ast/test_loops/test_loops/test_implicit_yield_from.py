# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    ImplicitYieldFromViolation,
)
from wemake_python_styleguide.visitors.ast.loops import (
    WrongLoopDefinitionVisitor,
)

for_loop_template = """
def function():
    for index in some:
        {0}
"""


@pytest.mark.parametrize('template', [
    for_loop_template,
])
@pytest.mark.parametrize('code', [
    'yield',
    'yield None',
    'yield index',
    'yield 10',
])
def test_implicit_yield_from(
    assert_errors,
    parse_ast_tree,
    code,
    template,
    default_options,
    regular_wrapper,
):
    """Ensures that implicit ``yield from`` are not allowed."""
    tree = parse_ast_tree(regular_wrapper(template.format(code)))

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImplicitYieldFromViolation])


@pytest.mark.parametrize('template', [
    for_loop_template,
])
@pytest.mark.parametrize('code', [
    'yield',
    'yield None',
    'yield index',
    'yield 10',
])
def test_async_implicit_yield_from(
    assert_errors,
    parse_ast_tree,
    code,
    template,
    default_options,
    async_wrapper,
):
    """Ensures that implicit ``yield from`` in async functions are allowed."""
    tree = parse_ast_tree(async_wrapper(template.format(code)))

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    for_loop_template,
])
@pytest.mark.parametrize('code', [
    'print(index)',
    'yield index\n        print(index)',
    'return index',
    'call(index)',
])
def test_correct_for_loop(
    assert_errors,
    parse_ast_tree,
    code,
    template,
    default_options,
    mode,
):
    """Ensures that correct ``for`` loops are allowed."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    for_loop_template,
])
@pytest.mark.parametrize('code', [
    'yield from index',
])
def test_correct_sync_for_loop(
    assert_errors,
    parse_ast_tree,
    code,
    template,
    default_options,
):
    """Ensures that correct ``for`` loops are allowed."""
    tree = parse_ast_tree(template.format(code))

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])

# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    InfiniteWhileLoopViolation,
)
from wemake_python_styleguide.visitors.ast.loops import WrongLoopVisitor

template_simple = """
while True:
    {0}
"""

template_nested_while1 = """
while True:
    while other:
        {0}
    {0}
"""

template_nested_while2 = """
while other:
    while True:
        {0}
    {0}
"""

template_nested_if = """
while True:
    if some:
        {0}
"""

template_function = """
def wrapper():
    while True:
        {0}
"""

template_other = """
while other:
    {0}
"""

# Double:

template_double_while = """
while True:
    while True:
        {0}
    {1}
"""


@pytest.mark.parametrize('template', [
    template_simple,
    template_nested_while1,
    template_nested_while2,
    template_nested_if,
    template_function,
    template_other,
])
@pytest.mark.parametrize('keyword', [
    'break',
    'raise Some',
    'raise Some()',
    'raise',
])
def test_correct_while_loops(
    assert_errors,
    parse_ast_tree,
    keyword,
    template,
    default_options,
):
    """Testing while loops with correct code."""
    tree = parse_ast_tree(template.format(keyword))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    template_function,
])
@pytest.mark.parametrize('keyword', [
    'return',
    'return some',
])
def test_correct_while_loops_function(
    assert_errors,
    parse_ast_tree,
    keyword,
    template,
    default_options,
    mode,
):
    """Testing while loops with ``return`` statements."""
    tree = parse_ast_tree(mode(template.format(keyword)))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    template_other,
])
@pytest.mark.parametrize('keyword', [
    'print(some)',
    'attr.method()',
    'a = 1',
])
def test_other_while_loops(
    assert_errors,
    parse_ast_tree,
    keyword,
    template,
    default_options,
):
    """Testing other while loops with regular code."""
    tree = parse_ast_tree(template.format(keyword))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    template_simple,
    template_nested_while1,
    template_nested_while2,
    template_nested_if,
    template_function,
])
@pytest.mark.parametrize('keyword', [
    'print(some)',
    'attr.method()',
    'a = 1',
])
def test_wrong_while_loops(
    assert_errors,
    parse_ast_tree,
    keyword,
    template,
    default_options,
):
    """Testing while loops with wrong code."""
    tree = parse_ast_tree(template.format(keyword))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InfiniteWhileLoopViolation])


@pytest.mark.parametrize('template', [
    template_double_while,
])
@pytest.mark.parametrize('keyword', [
    'break',
    'raise ValueError',
])
def test_double_while_correct_loops(
    assert_errors,
    parse_ast_tree,
    keyword,
    template,
    default_options,
):
    """Testing while loops with wrong code."""
    tree = parse_ast_tree(template.format(keyword, keyword))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    template_double_while,
])
@pytest.mark.parametrize(('keyword1', 'keyword2'), [
    ('print()', 'break'),
    ('break', 'other.attr = 1'),
])
def test_double_while_wrong_loops(
    assert_errors,
    parse_ast_tree,
    keyword1,
    keyword2,
    template,
    default_options,
):
    """Testing while loops with wrong code."""
    tree = parse_ast_tree(template.format(keyword1, keyword2))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InfiniteWhileLoopViolation])
